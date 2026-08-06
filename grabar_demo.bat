@echo off
echo ============================================
echo  GRABACION: Suite de pruebas Selenium (18)
echo ============================================
echo.

echo [1/3] Limpiando base de datos y evidencias...
del /q instance\database.db 2>nul
del /q screenshots\*.png 2>nul

echo [2/3] Iniciando servidor CRUD en http://127.0.0.1:5000 ...
start "CRUD Server" .venv\Scripts\python.exe run.py
timeout /t 6 /nobreak >nul

echo [3/3] Ejecutando pruebas (el navegador se vera abriendo y cerrando)...
echo.
.venv\Scripts\python.exe -m pytest -v

echo.
echo Deteniendo el servidor...
taskkill /f /im python.exe >nul 2>nul

echo.
echo ============================================
echo  FIN. Reporte HTML en report\report.html
echo  Evidencias en screenshots\
echo ============================================
pause
