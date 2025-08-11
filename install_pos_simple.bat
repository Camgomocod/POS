@echo off
chcp 65001 >nul
title Instalador Sistema POS - Windows 11 (Versión Simplificada)
color 0B

echo ╔══════════════════════════════════════════════════════════╗
echo ║            INSTALADOR SISTEMA POS - SIMPLE              ║
echo ║               Restaurante Fast Food v1.0                ║
echo ║                     Windows 11                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔍 Verificando requisitos del sistema...
echo.

REM Verificar Python
echo 📍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en PATH
    echo.
    echo 📥 INSTRUCCIONES PARA INSTALAR PYTHON:
    echo    1. Ir a: https://www.python.org/downloads/
    echo    2. Descargar Python 3.8 o superior
    echo    3. ✅ IMPORTANTE: Marcar "Add Python to PATH" durante la instalación
    echo    4. Reiniciar esta instalación después
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python encontrado: %PYTHON_VERSION%

REM Verificar pip
echo 📍 Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip no está disponible
    echo 📥 Instalando pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo ❌ Error al instalar pip
        pause
        exit /b 1
    )
)
echo ✅ pip disponible

echo.
echo 📁 Configurando entorno del proyecto...
set PROJECT_DIR=%~dp0
echo 📂 Directorio del proyecto: %PROJECT_DIR%

REM Crear entorno virtual
echo.
echo 📦 Creando entorno virtual Python...
if exist "venv" (
    echo 🔄 Entorno virtual existente encontrado, eliminando...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Error al crear entorno virtual
    echo 💡 Posibles soluciones:
    echo    - Ejecutar como administrador
    echo    - Verificar que Python esté correctamente instalado
    echo    - Verificar permisos en la carpeta del proyecto
    pause
    exit /b 1
)
echo ✅ Entorno virtual creado exitosamente

REM Activar entorno virtual
echo.
echo 🚀 Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error al activar entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado

REM Actualizar pip en el entorno virtual
echo.
echo 🔄 Actualizando pip en entorno virtual...
python -m pip install --upgrade pip --quiet
echo ✅ pip actualizado

REM Instalar dependencias
echo.
echo 📚 Instalando dependencias del proyecto...
echo    Esto puede tardar varios minutos...
echo.

if not exist "requirements.txt" (
    echo ❌ Archivo requirements.txt no encontrado
    pause
    exit /b 1
)

echo 📋 Dependencias a instalar:
type requirements.txt
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error al instalar dependencias
    echo.
    echo 💡 Posibles soluciones:
    echo    - Verificar conexión a internet
    echo    - Ejecutar como administrador
    echo    - Verificar que requirements.txt existe
    echo.
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas exitosamente

REM Verificar instalación
echo.
echo 🔍 Verificando instalación...
python -c "import PyQt5; print('✅ PyQt5:', PyQt5.Qt.QT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo ⚠️  Advertencia: PyQt5 podría no estar instalado correctamente
)

python -c "import sqlalchemy; print('✅ SQLAlchemy:', sqlalchemy.__version__)" 2>nul
if errorlevel 1 (
    echo ⚠️  Advertencia: SQLAlchemy podría no estar instalado correctamente
)

REM Verificar base de datos
echo.
echo 🗄️  Verificando base de datos...
if exist "data\pos.db" (
    echo ✅ Base de datos encontrada: data\pos.db
) else (
    echo ⚠️  Base de datos no encontrada, se creará automáticamente al primer uso
)

if exist "verify_clean_database.py" (
    echo 🔍 Ejecutando verificación de base de datos...
    python verify_clean_database.py
    if errorlevel 1 (
        echo ⚠️  Advertencia en verificación de base de datos
    ) else (
        echo ✅ Base de datos verificada correctamente
    )
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║               ✅ INSTALACIÓN COMPLETADA                  ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🎯 Para usar el Sistema POS:
echo.
echo    Opción 1: Ejecutar "run_pos.bat" desde esta carpeta
echo    Opción 2: Ejecutar "quick_start.bat" para inicio rápido
echo    Opción 3: Abrir cmd aquí y ejecutar: run_pos.bat
echo.
echo 🔗 Para crear acceso directo en el escritorio:
echo    Ejecutar: create_desktop_shortcut.ps1
echo    O usar: setup_master.bat (opción 3)
echo.
echo 👤 Credenciales por defecto:
echo    ┌─────────────────────────────────────────┐
echo    │ 👨‍💼 Administrador                        │
echo    │    Usuario: admin                       │
echo    │    Contraseña: admin123                 │
echo    │    Acceso: Completo al sistema          │
echo    └─────────────────────────────────────────┘
echo    ┌─────────────────────────────────────────┐
echo    │ 👨‍💻 Cajero                               │
echo    │    Usuario: cajero                      │
echo    │    Contraseña: cajero123                │
echo    │    Acceso: POS y operaciones básicas    │
echo    └─────────────────────────────────────────┘
echo.
echo ⚠️  IMPORTANTE PARA PRODUCCIÓN:
echo    - Cambiar las contraseñas por defecto
echo    - Configurar datos del restaurante en config.py
echo    - Probar todas las funcionalidades
echo.

set /p test_now="¿Deseas probar el sistema ahora? (s/n): "
if /i "%test_now%"=="s" (
    echo.
    echo 🚀 Iniciando Sistema POS...
    call run_pos.bat
) else (
    echo.
    echo 👋 ¡Instalación completada! Usa run_pos.bat para iniciar el sistema.
)

echo.
pause
