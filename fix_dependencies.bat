@echo off
chcp 65001 >nul
title Solución Rápida - Dependencias Faltantes
color 0A

echo ╔══════════════════════════════════════════════════════════╗
echo ║           SOLUCIÓN RÁPIDA - DEPENDENCIAS                ║
echo ║              Error: matplotlib/win32print               ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔧 Solucionando dependencias faltantes detectadas...
echo.

REM Verificar y activar entorno virtual
if exist "venv\Scripts\activate.bat" (
    echo ✅ Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Entorno virtual no encontrado
    echo 🔧 Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.
echo 📦 Instalando dependencias faltantes...
echo.

echo 📍 1/4: Instalando matplotlib...
pip install matplotlib>=3.5.0
if errorlevel 1 (
    echo ❌ Error instalando matplotlib
) else (
    echo ✅ matplotlib instalado correctamente
)

echo.
echo 📍 2/4: Instalando numpy...
pip install numpy>=1.21.0
if errorlevel 1 (
    echo ❌ Error instalando numpy
) else (
    echo ✅ numpy instalado correctamente
)

echo.
echo 📍 3/4: Instalando pywin32 (módulos de Windows)...
pip install pywin32>=304
if errorlevel 1 (
    echo ⚠️  Advertencia: pywin32 podría no instalarse correctamente
    echo 💡 Esto es normal, el sistema funcionará sin impresión avanzada
) else (
    echo ✅ pywin32 instalado correctamente
)

echo.
echo 📍 4/4: Verificando instalación...
python -c "import matplotlib; print('✅ matplotlib:', matplotlib.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ matplotlib aún no funciona
) else (
    echo ✅ matplotlib verificado
)

python -c "import numpy; print('✅ numpy:', numpy.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ numpy aún no funciona
) else (
    echo ✅ numpy verificado
)

python -c "import win32print; print('✅ win32print disponible')" 2>nul
if errorlevel 1 (
    echo ⚠️  win32print no disponible (solo advertencia)
) else (
    echo ✅ win32print verificado
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                  ✅ SOLUCIÓN APLICADA                    ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🎯 Dependencias críticas instaladas
echo.
echo 💡 Ahora puedes ejecutar el sistema con:
echo    • python main.py
echo    • run_pos.bat  
echo    • launcher_windows.bat
echo.

set /p test_now="¿Deseas probar el sistema ahora? (s/n): "
if /i "%test_now%"=="s" (
    echo.
    echo 🚀 Ejecutando Sistema POS...
    python main.py
) else (
    echo.
    echo 👋 Dependencias instaladas. Ejecuta python main.py cuando estés listo.
)

echo.
pause
