@echo off
rem ===================================================================
rem POS RestauranteFast - Launcher Mejorado para Windows 11
rem Launcher con mejor soporte de codificacion
rem ===================================================================

title POS RestauranteFast - Iniciando...
color 0A

rem Configurar codificacion UTF-8
chcp 65001 > nul 2>&1

rem Cambiar al directorio del script
cd /d "%~dp0"

rem Verificar que los archivos existen
if not exist "run_pos_windows.py" (
    echo.
    echo ===================================================================
    echo                           ERROR
    echo ===================================================================
    echo.
    echo No se encontro run_pos_windows.py en este directorio
    echo Directorio actual: %CD%
    echo.
    echo Asegurate de ejecutar este archivo desde la carpeta del proyecto POS
    echo.
    echo CREDENCIALES DE ACCESO:
    echo Admin:  admin / admin123
    echo Cajero: cajero / cajero123
    echo.
    pause
    exit /b 1
)

rem Intentar diferentes comandos de Python
echo Detectando Python...

rem Opcion 1: py (recomendado para Windows)
py --version >nul 2>&1
if %errorlevel%==0 (
    echo Python encontrado: py
    echo Ejecutando aplicacion...
    echo.
    py run_pos_windows.py
    goto :end
)

rem Opcion 2: python
python --version >nul 2>&1
if %errorlevel%==0 (
    echo Python encontrado: python
    echo Ejecutando aplicacion...
    echo.
    python run_pos_windows.py
    goto :end
)

rem Opcion 3: python3
python3 --version >nul 2>&1
if %errorlevel%==0 (
    echo Python encontrado: python3
    echo Ejecutando aplicacion...
    echo.
    python3 run_pos_windows.py
    goto :end
)

rem Buscar en ubicaciones comunes de Windows
set "PYTHON_PATHS="
set "PYTHON_PATHS=%PYTHON_PATHS%;C:\Python312\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS%;C:\Python311\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS%;C:\Python310\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS%;%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS%;%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe"
set "PYTHON_PATHS=%PYTHON_PATHS%;%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe"

for %%P in (%PYTHON_PATHS%) do (
    if exist "%%P" (
        echo Python encontrado: %%P
        echo Ejecutando aplicacion...
        echo.
        "%%P" run_pos_windows.py
        goto :end
    )
)

rem Si no se encuentra Python
echo.
echo ===================================================================
echo                           ERROR
echo ===================================================================
echo.
echo No se pudo encontrar Python en el sistema
echo.
echo SOLUCIONES POSIBLES:
echo 1. Instalar Python desde: https://python.org
echo 2. Verificar que Python este en PATH del sistema
echo 3. Reinstalar Python marcando "Add to PATH"
echo.
echo COMANDOS DE VERIFICACION:
echo py --version
echo python --version
echo python3 --version
echo.
echo CREDENCIALES DE ACCESO:
echo Admin:  admin / admin123
echo Cajero: cajero / cajero123
echo.

:end
echo.
if %errorlevel% neq 0 (
    echo ===================================================================
    echo La aplicacion termino con errores
    echo.
    echo CREDENCIALES DE ACCESO:
    echo Admin:  admin / admin123
    echo Cajero: cajero / cajero123
    echo ===================================================================
    echo.
    echo Presiona cualquier tecla para cerrar...
    pause >nul
) else (
    timeout /t 2 /nobreak >nul
)
