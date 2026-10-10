@echo off
REM Double-click to run Job Hunter on Windows.
cd /d "%~dp0"
where python >nul 2>nul || (echo Python is not installed. Get it at https://www.python.org/downloads/ and tick "Add Python to PATH". & pause & exit /b 1)
if not exist config.json (
  copy config.example.json config.json >nul
  echo Created config.json. Fill it in with your info, save it, then double-click run.bat again.
  notepad config.json
  exit /b 0
)
python -m pip install -q -r requirements.txt
python hunt.py
for /f %%d in ('python -c "import datetime;print(datetime.date.today())"') do start "" "output\%%d"
pause
