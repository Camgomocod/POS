@echo off
chcp 65001 >nul
title Sistema POS - Restaurante Fast v1.0
color 0A

:INICIO
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    SISTEMA POS v1.0                     ║
echo ║                 Restaurante Fast Food                   ║
echo ║                      Windows 11                         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🚀 Iniciando Sistema Point of Sale...
echo.

REM Verificar ubicación del script
if not exist "main.py" (
    echo ❌ Error: No se encuentra main.py
    echo 💡 Asegúrate de ejecutar este script desde la carpeta del proyecto POS
    echo 📁 Carpeta actual: %CD%
    echo.
    pause
    exit /b 1
)

REM Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en PATH
    echo 💡 Ejecuta install_pos_w11.bat para instalar dependencias
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% encontrado

REM Verificar y activar entorno virtual
echo.
echo 📦 Verificando entorno virtual...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Entorno virtual no encontrado
    echo 💡 Ejecuta install_pos_w11.bat para configurar el entorno
    echo.
    set /p install_now="¿Deseas ejecutar la instalación ahora? (s/n): "
    if /i "!install_now!"=="s" (
        call install_pos_w11.bat
        if errorlevel 1 (
            echo ❌ Error en la instalación
            pause
            exit /b 1
        )
    ) else (
        pause
        exit /b 1
    )
)

echo ✅ Entorno virtual encontrado
echo 🚀 Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error al activar entorno virtual
    echo 💡 Intenta eliminar la carpeta 'venv' y ejecutar install_pos_w11.bat
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado

REM Verificar dependencias críticas
echo.
echo 📚 Verificando dependencias...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyQt5 no está instalado
    echo 🔄 Instalando dependencias faltantes...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        echo 💡 Ejecuta install_pos_w11.bat para una instalación completa
        pause
        exit /b 1
    )
)
echo ✅ PyQt5 disponible

python -c "import sqlalchemy" >nul 2>&1
if errorlevel 1 (
    echo ❌ SQLAlchemy no está instalado
    echo 🔄 Instalando dependencias faltantes...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
)
echo ✅ SQLAlchemy disponible

REM Verificar base de datos
echo.
echo 🗄️  Verificando base de datos...
if exist "data\pos.db" (
    echo ✅ Base de datos encontrada
    for %%A in ("data\pos.db") do set db_size=%%~zA
    echo 📊 Tamaño: !db_size! bytes
) else (
    echo ⚠️  Base de datos no encontrada
    echo 🔄 Se creará automáticamente al iniciar la aplicación
    if not exist "data" mkdir data
)

REM Ejecutar verificación si existe
if exist "verify_clean_database.py" (
    echo 🔍 Verificando integridad de la base de datos...
    python verify_clean_database.py >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Advertencia: Problemas detectados en la base de datos
    ) else (
        echo ✅ Base de datos verificada correctamente
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                CREDENCIALES DE ACCESO                   ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║                                                          ║
echo ║  👨‍💼 ADMINISTRADOR                                        ║
echo ║     Usuario: admin                                       ║
echo ║     Contraseña: admin123                                 ║
echo ║     Acceso: Gestión completa del sistema                 ║
echo ║                                                          ║
echo ║  👨‍💻 CAJERO                                               ║
echo ║     Usuario: cajero                                      ║
echo ║     Contraseña: cajero123                                ║
echo ║     Acceso: POS y operaciones de venta                   ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo ⏳ Iniciando aplicación...
echo    Por favor espera mientras se carga la interfaz gráfica...
echo.

REM Verificar que main.py existe
if not exist "main.py" (
    echo ❌ Error: main.py no encontrado
    pause
    exit /b 1
)

REM Ejecutar aplicación
echo 🎯 Ejecutando Sistema POS...
python main.py

REM Manejar cierre de aplicación
set exit_code=%errorlevel%
echo.

if %exit_code% neq 0 (
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║              ❌ ERROR EN LA APLICACIÓN                   ║
    echo ╚══════════════════════════════════════════════════════════╝
    echo.
    echo 💥 La aplicación se cerró con errores (Código: %exit_code%)
    echo.
    echo 🔧 Posibles soluciones:
    echo    1. Verificar que todas las dependencias estén instaladas
    echo    2. Revisar la integridad de la base de datos
    echo    3. Ejecutar install_pos_w11.bat para reinstalar
    echo    4. Verificar permisos de archivos
    echo.
) else (
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║             ✅ APLICACIÓN CERRADA CORRECTAMENTE          ║
    echo ╚══════════════════════════════════════════════════════════╝
    echo.
    echo 👋 Sistema POS cerrado exitosamente
    echo.
)

:MENU_FINAL
echo ¿Qué deseas hacer a continuación?
echo.
echo [1] 🔄 Reiniciar la aplicación
echo [2] 📁 Abrir carpeta del proyecto
echo [3] 🔧 Ejecutar verificación de base de datos
echo [4] 📋 Ver información del sistema
echo [5] 🚪 Salir
echo.
set /p choice="Selecciona una opción (1-5): "

if "%choice%"=="1" goto INICIO
if "%choice%"=="2" (
    echo 📂 Abriendo carpeta del proyecto...
    explorer .
    goto MENU_FINAL
)
if "%choice%"=="3" (
    if exist "verify_clean_database.py" (
        echo 🔍 Ejecutando verificación...
        python verify_clean_database.py
    ) else (
        echo ❌ Script de verificación no encontrado
    )
    echo.
    pause
    goto MENU_FINAL
)
if "%choice%"=="4" (
    cls
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║               INFORMACIÓN DEL SISTEMA                   ║
    echo ╚══════════════════════════════════════════════════════════╝
    echo.
    echo 🖥️  Sistema Operativo: %OS%
    echo 📁 Directorio: %CD%
    python --version 2>&1
    echo.
    echo 📦 Dependencias instaladas:
    pip list | findstr -i "PyQt5 SQLAlchemy pandas openpyxl python-dateutil"
    echo.
    if exist "data\pos.db" (
        for %%A in ("data\pos.db") do echo 🗄️  Base de datos: %%~zA bytes
    )
    echo.
    pause
    goto MENU_FINAL
)
if "%choice%"=="5" (
    echo 👋 ¡Hasta luego!
    exit /b 0
)

echo ❌ Opción no válida, intenta de nuevo
goto MENU_FINAL
