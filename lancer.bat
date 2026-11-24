@echo off
start "Django" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python manage.py runserver"
start "React" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 6 >nul
start http://localhost:5173