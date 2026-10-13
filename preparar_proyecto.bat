@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 goto error

echo === Preparar InventariosAPP para desarrollo ===
echo Carpeta: %CD%
echo Este proceso conserva las bases de datos y usuarios existentes.
echo.

if exist ".venv\Scripts\python.exe" goto verificar_python
echo [1/5] Creando entorno virtual con Python 3.12...
py -3.12 -m venv .venv
if errorlevel 1 goto error_python

:verificar_python
".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 12) else 1)"
if errorlevel 1 goto error_python
echo [2/5] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo [3/5] Preparando carpeta de datos y aplicando migraciones...
".venv\Scripts\python.exe" -c "from config.settings import DATA_DIR; DATA_DIR.mkdir(parents=True, exist_ok=True); print('Datos de desarrollo:', DATA_DIR)"
if errorlevel 1 goto error
".venv\Scripts\python.exe" manage.py migrate
if errorlevel 1 goto error

echo [4/5] Preparando perfiles Lector y Operador...
".venv\Scripts\python.exe" manage.py configure_inventory_roles
if errorlevel 1 goto error

echo [5/5] Comprobando administrador...
".venv\Scripts\python.exe" manage.py shell -c "import sys; from django.contrib.auth import get_user_model; sys.exit(0 if get_user_model().objects.filter(is_superuser=True, is_active=True).exists() else 10)"
set "ADMIN_RESULT=%ERRORLEVEL%"
if "%ADMIN_RESULT%"=="0" goto administrador_existente
if not "%ADMIN_RESULT%"=="10" goto error
echo Escribe el usuario, correo y contrasena del administrador.
echo La contrasena no se muestra mientras la escribes.
".venv\Scripts\python.exe" manage.py createsuperuser
if errorlevel 1 goto error
goto listo

:administrador_existente
echo Ya existe un administrador activo. No se crea otra cuenta.

:listo
echo.
echo Preparacion completada. Ejecuta iniciar_desarrollo.bat para abrir Django.
if /I not "%~1"=="--sin-pausa" pause
exit /b 0

:error_python
echo.
echo No se pudo usar Python 3.12. Instala Python 3.12 con el lanzador py.
echo Si .venv ya existe con otra version, conservalo o renombralo antes de repetir.
goto error

:error
echo.
echo No se completo la preparacion. Revisa el error anterior y vuelve a intentarlo.
echo No se han eliminado tus datos ni el entorno existente.
if /I not "%~1"=="--sin-pausa" pause
exit /b 1
