# Assistive Navigation AI — Browser Camera Edition

A classroom/demo prototype. The phone browser opens its own camera and sends still frames to a Flask server on the laptop for YOLO object detection. It does **not** use the IP Webcam app.

## Requirements
- Windows 10/11 laptop
- Python 3.12 recommended (Python 3.10–3.12)
- Internet on laptop for package/model download
- Phone and laptop both online
- Google Chrome or another modern mobile browser

## Setup (Windows, beginner steps)

### 1. Extract the ZIP
Extract this folder somewhere simple, for example:
`C:\Users\user\Downloads\AssistiveNavigationAI_BrowserCamera`

### 2. Start the app
Double-click `START_APP.bat`.
- First run installs Python packages and can take several minutes.
- The YOLO model `yolov8n.pt` downloads automatically the first time AI detection is requested.
- Keep this terminal window open.
- When you see `Running on http://...:5000`, the local app is running.

### 3. Install Cloudflare Tunnel (one time)
Double-click `INSTALL_CLOUDFLARED.bat`.
If Windows asks for permission, approve the install. When finished, close and reopen terminal windows.

If winget is unavailable, install Cloudflare Tunnel (`cloudflared`) using Cloudflare's official Windows installation instructions.

### 4. Start the HTTPS link
Double-click `START_TUNNEL.bat` in a second window.
Wait for a URL ending in `.trycloudflare.com`, for example:
`https://some-words.trycloudflare.com`
Keep this window open too. This temporary link changes each time you restart the tunnel.

### 5. Create QR
On the laptop, open:
`http://127.0.0.1:5000/setup`
Paste the `https://....trycloudflare.com` URL from the tunnel window and click **Save link & create QR**.

### 6. Open on phone
Scan the QR code. The phone should open the HTTPS website.
Tap **Allow camera & start AI** and approve camera permission.
The browser should use the rear camera if available.

## Troubleshooting
- **No camera permission / insecure page:** Make sure the phone opened the `https://...trycloudflare.com` link, not `http://<laptop-ip>:5000`.
- **Phone can't open page:** Check both devices have internet and both app/tunnel terminal windows are still running.
- **AI model taking time:** First model download can take a few minutes. Keep the laptop online.
- **Python not found:** Install Python 3.12 and tick "Add Python to PATH", then run `START_APP.bat` again.
- **Port 5000 in use:** Close the old Flask app terminal or stop the old server before starting this one.

## Safety and limitations
This is an experimental demo only. The pretrained model recognises a limited set of common objects and can miss or misclassify things. It does not measure physical distance, reliably determine collision risk, detect every hazard, or provide dependable navigation. It must not be used as a replacement for a cane, guide dog, or human assistance. Test only while stationary in a safe place.
