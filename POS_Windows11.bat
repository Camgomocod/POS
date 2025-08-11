@echo off
rem ===================================================================
rem POS RestauranteFast - Launcher para Windows 11
rem Detecta automaticamente Python y ejecuta la aplicacion
rem ===================================================================

title POS RestauranteFast - Iniciando...
color 0A

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║                    POS RestauranteFast                        ║
echo  ║              Sistema de Punto de Venta                       ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.
echo  🚀 Iniciando aplicacion...

rem Cambiar al directorio del script
cd /d "%~dp0"

rem Verificar que main.py existe
if not exist "main.py" (
    echo  ❌ Error: No se encontro main.py en este directorio
    echo  📁 Directorio actual: %CD%
    echo.
    echo  💡 Asegurate de ejecutar este archivo desde la carpeta del proyecto POS
    pause
    exit /b 1
)

rem Intentar diferentes comandos de Python
echo  🔍 Detectando Python...

rem Opcion 1: py (recomendado para Windows)
py --version >nul 2>&1
if %errorlevel%==0 (
    echo  ✅ Python encontrado: py
    echo  🎯 Ejecutando aplicacion...
    echo.
    py main.py
    goto :end
)

rem Opcion 2: python
python --version >nul 2>&1
if %errorlevel%==0 (
    echo  ✅ Python encontrado: python
    echo  🎯 Ejecutando aplicacion...
    echo.
    python main.py
    goto :end
)

rem Opcion 3: python3
python3 --version >nul 2>&1
if %errorlevel%==0 (
    echo  ✅ Python encontrado: python3
    echo  🎯 Ejecutando aplicacion...
    echo.
    python3 main.py
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
        echo  ✅ Python encontrado: %%P
        echo  🎯 Ejecutando aplicacion...
        echo.
        "%%P" main.py
        goto :end
    )
)

rem Si no se encuentra Python
echo  ❌ Error: No se pudo encontrar Python en el sistema
echo.
echo  📋 SOLUCIONES POSIBLES:
echo  ────────────────────────────────────────────────────────────────
echo  1. Instalar Python desde: https://python.org
echo  2. Verificar que Python este en PATH del sistema
echo  3. Reinstalar Python marcando "Add to PATH"
echo.
echo  🔧 COMANDOS DE VERIFICACION:
echo  ────────────────────────────────────────────────────────────────
echo  py --version
echo  python --version
echo  python3 --version
echo.

:end
echo.
if %errorlevel% neq 0 (
    echo  ❌ La aplicacion termino con errores
    echo.
    echo  📋 CREDENCIALES DE ACCESO:
    echo  ────────────────────────────────────────────────────────────────
    echo  👑 Admin: admin / admin123
    echo  💰 Cajero: cajero / cajero123
    echo.
    echo  💡 Presiona cualquier tecla para cerrar...
    pause >nul
) else (
    echo  ✅ Aplicacion cerrada correctamente
    timeout /t 3 /nobreak >nul
)
