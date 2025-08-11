@echo off
chcp 65001 >nul
title Diagnóstico Sistema POS - Windows 11
color 0E

echo ╔══════════════════════════════════════════════════════════╗
echo ║              DIAGNÓSTICO COMPLETO - SISTEMA POS         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔍 Realizando diagnóstico completo...
echo.

REM Verificar ubicación actual
echo 📍 Ubicación actual:
echo    %CD%
echo.

REM Verificar archivos principales
echo 📁 Verificando archivos del proyecto:
if exist "main.py" (
    echo    ✅ main.py encontrado
) else (
    echo    ❌ main.py NO encontrado
)

if exist "requirements.txt" (
    echo    ✅ requirements.txt encontrado
) else (
    echo    ❌ requirements.txt NO encontrado
)

if exist "config.py" (
    echo    ✅ config.py encontrado
) else (
    echo    ⚠️  config.py no encontrado
)

echo.

REM Verificar Python
echo 🐍 Verificando Python:
python --version 2>nul
if errorlevel 1 (
    echo    ❌ Python NO está disponible
    echo    💡 Instalar Python desde python.org y marcar "Add to PATH"
) else (
    echo    ✅ Python disponible
    python -c "import sys; print('    📂 Ejecutable:', sys.executable)"
    python -c "import sys; print('    📋 Versión:', sys.version.split()[0])"
)

echo.

REM Verificar entorno virtual
echo 🏠 Verificando entorno virtual:
if exist "venv" (
    echo    ✅ Carpeta venv existe
    if exist "venv\Scripts\python.exe" (
        echo    ✅ Python en venv disponible
    ) else (
        echo    ❌ Python en venv NO disponible
    )
    
    if exist "venv\Scripts\activate.bat" (
        echo    ✅ Script de activación existe
    ) else (
        echo    ❌ Script de activación NO existe
    )
) else (
    echo    ❌ Entorno virtual NO existe
)

echo.

REM Probar activación de entorno virtual
echo 🚀 Probando activación de entorno virtual:
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat >nul 2>&1
    if errorlevel 1 (
        echo    ❌ Error al activar entorno virtual
    ) else (
        echo    ✅ Entorno virtual activado correctamente
        
        echo.
        echo 📦 Verificando dependencias instaladas:
        python -c "import PyQt5; print('    ✅ PyQt5:', PyQt5.Qt.QT_VERSION_STR)" 2>nul
        if errorlevel 1 (
            echo    ❌ PyQt5 NO está instalado
        )
        
        python -c "import sqlalchemy; print('    ✅ SQLAlchemy:', sqlalchemy.__version__)" 2>nul
        if errorlevel 1 (
            echo    ❌ SQLAlchemy NO está instalado
        )
        
        python -c "import pandas; print('    ✅ Pandas:', pandas.__version__)" 2>nul
        if errorlevel 1 (
            echo    ❌ Pandas NO está instalado
        )
    )
) else (
    echo    ❌ No se puede probar - entorno virtual no existe
)

echo.

REM Verificar base de datos
echo 🗄️  Verificando base de datos:
if exist "data" (
    echo    ✅ Carpeta data existe
    if exist "data\pos.db" (
        for %%A in ("data\pos.db") do echo    ✅ Base de datos: %%~zA bytes
    ) else (
        echo    ⚠️  Base de datos no existe (se creará automáticamente)
    )
) else (
    echo    ⚠️  Carpeta data no existe
)

echo.

REM Probar ejecución básica
echo 🧪 Probando ejecución básica:
if exist "main.py" (
    if exist "venv\Scripts\activate.bat" (
        echo    🔄 Probando importaciones básicas...
        call venv\Scripts\activate.bat >nul 2>&1
        python -c "print('✅ Python funciona')" 2>nul
        if errorlevel 1 (
            echo    ❌ Error en Python básico
        ) else (
            python -c "import sys; print('✅ Importación básica funciona')" 2>nul
            python -c "import os; print('✅ Módulos OS funcionan')" 2>nul
            
            echo    🔄 Probando PyQt5...
            python -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 importa correctamente')" 2>nul
            if errorlevel 1 (
                echo    ❌ PyQt5 no funciona correctamente
            ) else (
                echo    🔄 Probando creación de QApplication...
                python -c "import sys; from PyQt5.QtWidgets import QApplication; app = QApplication(sys.argv); print('✅ QApplication se puede crear'); app.quit()" 2>nul
                if errorlevel 1 (
                    echo    ❌ No se puede crear QApplication (problema de entorno gráfico)
                ) else (
                    echo    ✅ QApplication funciona correctamente
                )
            )
        )
    ) else (
        echo    ❌ No se puede probar - entorno virtual no disponible
    )
) else (
    echo    ❌ No se puede probar - main.py no encontrado
)

echo.

REM Verificar variables de entorno importantes
echo 🌍 Variables de entorno:
echo    DISPLAY=%DISPLAY%
echo    PATH contiene Python: 
python -c "import sys, os; print('    ✅ Sí' if any('python' in p.lower() for p in os.environ.get('PATH', '').split(';')) else '    ❌ No')" 2>nul

echo.

REM Diagnóstico de Windows
echo 🖥️  Información del sistema:
echo    Sistema: %OS%
echo    Computadora: %COMPUTERNAME%
echo    Usuario: %USERNAME%

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                  RESUMEN DEL DIAGNÓSTICO                ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

if not exist "main.py" (
    echo ❌ PROBLEMA CRÍTICO: Archivos del proyecto no encontrados
    echo 💡 Solución: Verificar que estás en la carpeta correcta del proyecto
    echo.
)

if not exist "venv" (
    echo ❌ PROBLEMA CRÍTICO: Entorno virtual no existe
    echo 💡 Solución: Ejecutar install_pos_simple.bat
    echo.
)

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PROBLEMA CRÍTICO: Python no está disponible
    echo 💡 Solución: Instalar Python desde python.org y marcar "Add to PATH"
    echo.
)

echo 📋 Próximos pasos recomendados:
echo.
echo    1. Si Python no está disponible: Instalar Python
echo    2. Si faltan archivos: Verificar ubicación del proyecto  
echo    3. Si no hay entorno virtual: Ejecutar install_pos_simple.bat
echo    4. Si PyQt5 falla: Problema de entorno gráfico de Windows
echo.

pause
