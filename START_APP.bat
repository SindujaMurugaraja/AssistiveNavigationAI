@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating Python virtual environment...
  py -3.12 -m venv .venv
  if errorlevel 1 py -3 -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
pause
