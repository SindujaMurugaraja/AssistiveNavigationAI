
from flask import Flask, render_template, request, jsonify, send_file
from threading import Lock
import base64
import cv2
import numpy as np
import qrcode
import io
import socket

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

model = None
model_lock = Lock()
public_url = ""


def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    except OSError:
        return "127.0.0.1"

    finally:
        s.close()


def load_model():
    global model

    if model is None:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")

    return model


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/setup")
def setup():
    return render_template("setup.html", public_url=public_url)


@app.route("/set-public-url", methods=["POST"])
def set_public_url():
    global public_url

    value = (request.json or {}).get("url", "").strip().rstrip("/")

    if not value.startswith("https://"):
        return jsonify({
            "ok": False,
            "error": "Paste the HTTPS trycloudflare.com link."
        }), 400

    public_url = value

    return jsonify({
        "ok": True,
        "url": public_url
    })


@app.route("/qr.png")
def qr_png():

    if not public_url:
        return "Set the HTTPS link on the setup page first.", 400

    img = qrcode.make(public_url)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return send_file(buf, mimetype="image/png")


@app.route("/api/detect", methods=["POST"])
def detect():

    data = request.get_json(silent=True) or {}

    image_data = data.get("image", "")

    if "," in image_data:
        image_data = image_data.split(",", 1)[1]

    if not image_data:
        return jsonify({
            "ok": False,
            "error": "No camera frame received."
        }), 400

    try:

        raw = base64.b64decode(image_data, validate=True)

        arr = np.frombuffer(raw, dtype=np.uint8)

        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        if frame is None:
            raise ValueError("Could not decode camera frame.")

        frame_height, frame_width = frame.shape[:2]

        with model_lock:

            detector = load_model()

            results = detector.predict(
                frame,
                imgsz=640,
                conf=0.40,
                verbose=False
            )

        items = []

        for result in results:

            names = result.names

            if result.boxes is None:
                continue

            for box in result.boxes:

                cls_id = int(box.cls[0].item())

                confidence = float(box.conf[0].item())

                xyxy = [
                    round(float(x), 1)
                    for x in box.xyxy[0].tolist()
                ]

                items.append({

                    "name": str(names.get(cls_id, cls_id)),

                    "confidence": round(confidence, 2),

                    "box": xyxy,

                    "frame_width": frame_width,

                    "frame_height": frame_height

                })

        return jsonify({

            "ok": True,

            "objects": items,

            "frame": {
                "width": frame_width,
                "height": frame_height
            }

        })

    except Exception as exc:

        app.logger.exception("Object detection failed")

        return jsonify({
            "ok": False,
            "error": str(exc)
        }), 500


@app.route("/health")
def health():

    return jsonify({
        "ok": True,
        "message": "Assistive Navigation AI server is running."
    })


if __name__ == "__main__":

    ip = get_lan_ip()

    print("\nASSISTIVE NAVIGATION AI - BROWSER CAMERA")

    print("Laptop setup page: http://127.0.0.1:5000/setup")

    print(f"Local app:          http://{ip}:5000")

    print("\nKeep this window open while using the app.\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
