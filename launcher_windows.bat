@echo off
chcp 65001 >nul
title Sistema POS - Launcher Windows 11
color 0A

REM Configurar variables para entorno gráfico
set QT_AUTO_SCREEN_SCALE_FACTOR=1
set QT_SCALE_FACTOR=1
set QT_SCREEN_SCALE_FACTORS=1

echo ╔══════════════════════════════════════════════════════════╗
echo ║             SISTEMA POS - LAUNCHER WINDOWS 11           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Verificaciones básicas
if not exist "main.py" (
    echo ❌ Error: main.py no encontrado
    echo 📁 Ubicación actual: %CD%
    echo 💡 Asegúrate de estar en la carpeta del proyecto POS
    pause
    exit /b 1
)

echo ✅ Proyecto POS detectado
echo 📁 Ubicación: %CD%
echo.

REM Verificar y activar entorno virtual
if exist "venv\Scripts\activate.bat" (
    echo 🚀 Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️  Entorno virtual no encontrado
    echo 💡 Usando Python del sistema
)

echo.

REM Verificar dependencias críticas
echo 🔍 Verificando dependencias...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyQt5 no está instalado
    echo 🔄 Intentando instalar dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        echo 💡 Ejecuta install_pos_simple.bat primero
        pause
        exit /b 1
    )
) else (
    echo ✅ PyQt5 disponible
)

REM Configurar entorno para mejor compatibilidad con Windows
echo 🖥️  Configurando entorno gráfico...
set QT_QPA_PLATFORM_PLUGIN_PATH=%CD%\venv\Lib\site-packages\PyQt5\Qt\plugins
set QT_PLUGIN_PATH=%CD%\venv\Lib\site-packages\PyQt5\Qt\plugins

echo.
echo 👤 Credenciales del sistema:
echo    Admin: admin / admin123
echo    Cajero: cajero / cajero123
echo.

echo 🚀 Iniciando Sistema POS...
echo    Si no se abre la ventana, revisa si hay errores abajo
echo.

REM Ejecutar con mejor manejo de errores
python -u main.py
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE% neq 0 (
    echo ❌ La aplicación terminó con errores (Código: %EXIT_CODE%)
    echo.
    echo 🔧 Posibles soluciones:
    echo    1. Ejecutar diagnostico_sistema.bat para más información
    echo    2. Verificar que todas las dependencias estén instaladas
    echo    3. Probar con install_pos_simple.bat
    echo.
) else (
    echo ✅ Aplicación cerrada correctamente
)

pause
