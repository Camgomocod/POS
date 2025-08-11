@echo off
chcp 65001 >nul
title Solucionador de Problemas POS Windows 11
color 0C

echo ╔══════════════════════════════════════════════════════════╗
echo ║         SOLUCIONADOR DE PROBLEMAS - SISTEMA POS         ║
echo ║                    Windows 11                           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:MENU_PRINCIPAL
echo 🛠️  ¿Cuál es tu problema?
echo.
echo [1] 🐍 Python main.py no hace nada (no abre ventana)
echo [2] 📦 Los archivos .bat no se reconocen como comandos
echo [3] 🔧 Error "Módulo no encontrado" 
echo [4] 🖥️  Error de entorno gráfico/display
echo [5] 🔄 Reinstalar todo desde cero
echo [6] 🧪 Ejecutar diagnóstico completo
echo [7] 🚪 Salir
echo.
set /p choice="Selecciona el problema (1-7): "

if "%choice%"=="1" goto PROBLEM_NO_WINDOW
if "%choice%"=="2" goto PROBLEM_BAT_FILES
if "%choice%"=="3" goto PROBLEM_MODULES
if "%choice%"=="4" goto PROBLEM_DISPLAY
if "%choice%"=="5" goto PROBLEM_REINSTALL
if "%choice%"=="6" goto PROBLEM_DIAGNOSTIC
if "%choice%"=="7" goto EXIT

echo ❌ Opción no válida
timeout /t 2 >nul
goto MENU_PRINCIPAL

:PROBLEM_NO_WINDOW
cls
echo 🐍 PROBLEMA: python main.py no abre ventana
echo ================================================
echo.
echo 🔍 Diagnosticando problema...
echo.

REM Verificar si está en el directorio correcto
if not exist "main.py" (
    echo ❌ No estás en la carpeta del proyecto POS
    echo 💡 Navega a la carpeta que contiene main.py
    pause
    goto MENU_PRINCIPAL
)

echo ✅ main.py encontrado
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🚀 Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No hay entorno virtual, usando Python del sistema
)

echo.
echo 🧪 Probando PyQt5...
python test_pyqt5.py
echo.

echo 🔧 Soluciones a probar:
echo.
echo [1] 🖥️  Usar launcher especial para Windows
echo [2] 🔄 Reinstalar PyQt5
echo [3] 🧪 Probar con modo verboso
echo [4] 🔙 Volver al menú principal
echo.
set /p fix_choice="Selecciona solución (1-4): "

if "%fix_choice%"=="1" (
    echo 🚀 Ejecutando launcher especial...
    call launcher_windows.bat
)
if "%fix_choice%"=="2" (
    echo 🔄 Reinstalando PyQt5...
    pip uninstall -y PyQt5
    pip install PyQt5==5.15.9
    echo ✅ PyQt5 reinstalado, probando...
    call launcher_windows.bat
)
if "%fix_choice%"=="3" (
    echo 🧪 Ejecutando en modo verboso...
    python -u -v main.py
    pause
)
if "%fix_choice%"=="4" goto MENU_PRINCIPAL

pause
goto MENU_PRINCIPAL

:PROBLEM_BAT_FILES
cls
echo 📦 PROBLEMA: Archivos .bat no se reconocen
echo ================================================
echo.
echo 🔍 Causa común: Ruta con espacios o caracteres especiales
echo.
echo 📁 Ubicación actual: %CD%
echo.

REM Verificar si la ruta tiene espacios
echo %CD% | findstr " " >nul
if not errorlevel 1 (
    echo ❌ PROBLEMA DETECTADO: La ruta contiene espacios
    echo.
    echo 💡 SOLUCIÓN:
    echo    1. Crea una carpeta sin espacios: C:\POS\
    echo    2. Mueve todo el proyecto ahí
    echo    3. Ejecuta los scripts desde la nueva ubicación
    echo.
) else (
    echo ✅ La ruta no contiene espacios
    echo.
    echo 🔧 Otras soluciones:
    echo    1. Ejecutar CMD como administrador
    echo    2. Verificar que los archivos .bat existen
    echo    3. Usar rutas completas: C:\ruta\archivo.bat
    echo.
)

echo 📋 Archivos .bat disponibles:
if exist "install_pos_simple.bat" echo    ✅ install_pos_simple.bat
if exist "launcher_windows.bat" echo    ✅ launcher_windows.bat  
if exist "diagnostico_sistema.bat" echo    ✅ diagnostico_sistema.bat
if exist "run_pos.bat" echo    ✅ run_pos.bat

echo.
set /p test_bat="¿Probar ejecutar launcher_windows.bat ahora? (s/n): "
if /i "%test_bat%"=="s" call launcher_windows.bat

pause
goto MENU_PRINCIPAL

:PROBLEM_MODULES
cls
echo 🔧 PROBLEMA: Error "Módulo no encontrado"
echo ================================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo 🚀 Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ❌ No hay entorno virtual
    echo 💡 Ejecuta: install_pos_simple.bat
    pause
    goto MENU_PRINCIPAL
)

echo.
echo 📦 Dependencias actuales:
pip list | findstr -i "PyQt5 SQLAlchemy pandas openpyxl python-dateutil"

echo.
echo 🔄 Reinstalando todas las dependencias...
pip install --force-reinstall -r requirements.txt

echo.
echo ✅ Dependencias reinstaladas
echo 🧪 Probando importaciones...
python -c "import PyQt5; print('✅ PyQt5 OK')"
python -c "import sqlalchemy; print('✅ SQLAlchemy OK')"
python -c "import pandas; print('✅ Pandas OK')"

pause
goto MENU_PRINCIPAL

:PROBLEM_DISPLAY
cls
echo 🖥️  PROBLEMA: Error de entorno gráfico
echo ================================================
echo.

echo 🔧 Configurando variables de entorno para PyQt5...
set QT_QPA_PLATFORM=windows
set QT_AUTO_SCREEN_SCALE_FACTOR=1
set QT_SCALE_FACTOR=1

echo ✅ Variables configuradas
echo.

if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat

echo 🧪 Probando con configuración especial...
python test_pyqt5.py

echo.
echo 🚀 Intentando ejecutar con configuración corregida...
call launcher_windows.bat

pause
goto MENU_PRINCIPAL

:PROBLEM_REINSTALL
cls
echo 🔄 REINSTALACIÓN COMPLETA
echo ================================================
echo.
echo ⚠️  Esto eliminará el entorno virtual actual y reinstalará todo
set /p confirm="¿Continuar? (s/n): "
if /i not "%confirm%"=="s" goto MENU_PRINCIPAL

echo.
echo 🗑️  Eliminando entorno virtual...
if exist "venv" rmdir /s /q venv

echo 📦 Creando nuevo entorno virtual...
python -m venv venv
call venv\Scripts\activate.bat

echo 📚 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo 🧪 Probando instalación...
python test_pyqt5.py

echo.
echo ✅ Reinstalación completada
echo 🚀 Probando aplicación...
call launcher_windows.bat

pause
goto MENU_PRINCIPAL

:PROBLEM_DIAGNOSTIC
cls
echo 🧪 DIAGNÓSTICO COMPLETO
echo ================================================
echo.

call diagnostico_sistema.bat

pause
goto MENU_PRINCIPAL

:EXIT
echo.
echo 👋 ¡Esperamos que hayas solucionado el problema!
echo.
echo 💡 Si sigues teniendo problemas:
echo    - Revisa que Python esté correctamente instalado
echo    - Verifica que estás en la carpeta correcta del proyecto
echo    - Intenta mover el proyecto a una ruta sin espacios
echo    - Ejecuta como administrador
echo.
pause
exit /b 0
