@echo off
chcp 65001 >nul
title Verificación de Requisitos - Sistema POS
color 0E

echo ╔══════════════════════════════════════════════════════════╗
echo ║             VERIFICACIÓN DE REQUISITOS                  ║
echo ║                   Sistema POS v1.0                      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

set ERROR_COUNT=0
set WARNING_COUNT=0

echo 🔍 Verificando requisitos del sistema para Windows 11...
echo.

REM Verificar versión de Windows
echo 📋 Sistema Operativo:
ver
echo.

REM Verificar Python
echo 📍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python NO está instalado o no está en PATH
    echo 💡 Solución: Instalar Python desde https://python.org
    echo    ✅ Marcar "Add Python to PATH" durante la instalación
    set /a ERROR_COUNT+=1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python !PYTHON_VERSION! encontrado
    
    REM Verificar versión mínima de Python (3.7+)
    for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VERSION!") do (
        if %%a LSS 3 (
            echo ⚠️  Versión de Python muy antigua (se requiere 3.7+)
            set /a WARNING_COUNT+=1
        ) else if %%a EQU 3 if %%b LSS 7 (
            echo ⚠️  Versión de Python muy antigua (se requiere 3.7+)
            set /a WARNING_COUNT+=1
        ) else (
            echo ✅ Versión de Python compatible
        )
    )
)

REM Verificar pip
echo.
echo 📍 Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip NO está disponible
    echo 💡 Solución: Reinstalar Python con pip incluido
    set /a ERROR_COUNT+=1
) else (
    for /f "tokens=2" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
    echo ✅ pip !PIP_VERSION! disponible
)

REM Verificar conexión a internet
echo.
echo 📍 Verificando conexión a internet...
ping -n 1 pypi.org >nul 2>&1
if errorlevel 1 (
    echo ⚠️  No se puede conectar a PyPI (repositorio de Python)
    echo 💡 Verificar conexión a internet para instalar dependencias
    set /a WARNING_COUNT+=1
) else (
    echo ✅ Conexión a PyPI disponible
)

REM Verificar permisos de escritura
echo.
echo 📍 Verificando permisos de escritura...
echo test > test_write.tmp 2>nul
if exist test_write.tmp (
    del test_write.tmp
    echo ✅ Permisos de escritura disponibles
) else (
    echo ⚠️  Permisos de escritura limitados
    echo 💡 Considerar ejecutar como administrador
    set /a WARNING_COUNT+=1
)

REM Verificar espacio en disco
echo.
echo 📍 Verificando espacio en disco...
for /f "tokens=3" %%i in ('dir /-c ^| find "bytes free"') do set FREE_SPACE=%%i
if defined FREE_SPACE (
    echo ✅ Espacio libre disponible
) else (
    echo ⚠️  No se pudo verificar espacio en disco
    set /a WARNING_COUNT+=1
)

REM Verificar archivos del proyecto
echo.
echo 📍 Verificando archivos del proyecto...

if exist "main.py" (
    echo ✅ main.py encontrado
) else (
    echo ❌ main.py NO encontrado
    echo 💡 Asegúrate de estar en la carpeta correcta del proyecto
    set /a ERROR_COUNT+=1
)

if exist "requirements.txt" (
    echo ✅ requirements.txt encontrado
    echo 📋 Dependencias requeridas:
    type requirements.txt | findstr /v "^$"
) else (
    echo ❌ requirements.txt NO encontrado
    set /a ERROR_COUNT+=1
)

if exist "config.py" (
    echo ✅ config.py encontrado
) else (
    echo ⚠️  config.py no encontrado
    set /a WARNING_COUNT+=1
)

REM Verificar estructura de carpetas
echo.
echo 📍 Verificando estructura del proyecto...
set REQUIRED_FOLDERS=controllers models utils views data

for %%f in (%REQUIRED_FOLDERS%) do (
    if exist "%%f" (
        echo ✅ Carpeta %%f encontrada
    ) else (
        echo ⚠️  Carpeta %%f no encontrada
        set /a WARNING_COUNT+=1
    )
)

REM Verificar entorno virtual si existe
echo.
echo 📍 Verificando entorno virtual...
if exist "venv" (
    if exist "venv\Scripts\activate.bat" (
        echo ✅ Entorno virtual configurado correctamente
    ) else (
        echo ⚠️  Entorno virtual incompleto
        echo 💡 Eliminar carpeta 'venv' y ejecutar install_pos_w11.bat
        set /a WARNING_COUNT+=1
    )
) else (
    echo ℹ️  Entorno virtual no configurado (se creará durante la instalación)
)

REM Verificar si ya hay dependencias instaladas globalmente
echo.
echo 📍 Verificando dependencias globales...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ℹ️  PyQt5 no instalado globalmente
) else (
    echo ✅ PyQt5 disponible globalmente
)

python -c "import sqlalchemy" >nul 2>&1
if errorlevel 1 (
    echo ℹ️  SQLAlchemy no instalado globalmente
) else (
    echo ✅ SQLAlchemy disponible globalmente
)

REM Resumen final
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                   RESUMEN DE VERIFICACIÓN               ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

if %ERROR_COUNT% EQU 0 (
    if %WARNING_COUNT% EQU 0 (
        echo ✅ ¡PERFECTO! Todos los requisitos están satisfechos
        echo 🚀 El sistema está listo para la instalación
        echo.
        echo 📋 Próximos pasos:
        echo    1. Ejecutar install_pos_w11.bat para instalar dependencias
        echo    2. Usar run_pos.bat para ejecutar el sistema
    ) else (
        echo ✅ Sistema compatible con advertencias menores
        echo ⚠️  %WARNING_COUNT% advertencia(s) encontrada(s)
        echo 🚀 La instalación debería funcionar correctamente
        echo.
        echo 📋 Próximos pasos:
        echo    1. Revisar las advertencias mostradas arriba
        echo    2. Ejecutar install_pos_w11.bat para instalar
    )
) else (
    echo ❌ Se encontraron %ERROR_COUNT% error(es) crítico(s)
    if %WARNING_COUNT% GTR 0 echo ⚠️  Y %WARNING_COUNT% advertencia(s)
    echo.
    echo 🔧 REQUISITOS FALTANTES:
    echo    - Revisar todos los errores marcados con ❌
    echo    - Instalar Python 3.7+ con pip si es necesario
    echo    - Verificar que estás en la carpeta correcta del proyecto
    echo.
    echo 💡 Una vez corregidos los errores, ejecuta install_pos_w11.bat
)

echo.
echo 📊 Estadísticas:
echo    - Errores críticos: %ERROR_COUNT%
echo    - Advertencias: %WARNING_COUNT%
echo    - Directorio actual: %CD%
echo    - Fecha/Hora: %DATE% %TIME%

echo.
pause
