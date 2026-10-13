@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 goto error
if not exist ".venv\Scripts\python.exe" goto falta_entorno

echo === InventariosAPP - servidor de desarrollo ===
echo Abre http://127.0.0.1:8000/admin/ en tu navegador.
echo Ingresa con tu usuario administrador.
echo Deten el servidor con Ctrl+C. Mantiene esta consola abierta.
echo.
".venv\Scripts\python.exe" manage.py runserver
if errorlevel 1 goto error
exit /b 0

:falta_entorno
echo Primero ejecuta preparar_proyecto.bat.

:error
echo.
echo El servidor no esta ejecutandose. Revisa el mensaje anterior.
if /I not "%~1"=="--sin-pausa" pause
exit /b 1
