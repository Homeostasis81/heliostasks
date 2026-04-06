@echo off
title Helios Tasks - Система за задачи
color 0E
echo.
echo  ============================================
echo    HELIOS TASKS - Система за задачи
echo    Helios Yachts AD
echo  ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python не е намерен!
    echo  Моля, инсталирайте Python 3.11+
    echo  https://www.python.org/downloads/
    pause
    exit /b
)

:: Install dependencies
echo  [*] Инсталиране на зависимости...
pip install -r requirements.txt -q

echo.
echo  [*] Стартиране на сървъра...
echo.
echo  ============================================
echo    Отворете в браузър:
echo    http://localhost:8000
echo.
echo    CEO вход: drago / helios2026
echo    Служители: ivan, maria, petar,
echo                georgi, elena / 1234
echo  ============================================
echo.

:: Start server
python -m uvicorn app:app --host 0.0.0.0 --port 8000

pause
