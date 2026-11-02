@echo off
echo Installing Cloudflare Tunnel using Windows Package Manager...
winget install --id Cloudflare.cloudflared -e
echo.
echo If installation succeeded, close this window and open a NEW terminal.
pause
