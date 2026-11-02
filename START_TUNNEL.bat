@echo off
echo Starting a temporary HTTPS tunnel to your local Flask app...
cloudflared tunnel --url http://localhost:5000
pause
