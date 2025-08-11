@echo off
chcp 65001 >nul
title Solución Error -1073741819 - Sistema POS
color 0C

echo ╔══════════════════════════════════════════════════════════╗
echo ║         SOLUCIÓN ERROR -1073741819 (Access Violation)   ║
echo ║                    Sistema POS v1.0                     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔍 Error detectado: -1073741819 (0xC0000005)
echo 💡 Causa: Access Violation - Problema de memoria/gráficos
echo.

echo 🔧 Aplicando soluciones paso a paso...
echo.

REM ============================================================================
echo 📍 PASO 1: Configurar variables de entorno PyQt5
echo ============================================================================

echo Configurando variables críticas para PyQt5...
set QT_QPA_PLATFORM=windows
set QT_AUTO_SCREEN_SCALE_FACTOR=0
set QT_SCALE_FACTOR=1
set QT_DEVICE_PIXEL_RATIO=1
set QT_ENABLE_HIGHDPI_SCALING=0
set QT_FONT_DPI=96

echo ✅ Variables de entorno configuradas

REM ============================================================================
echo.
echo 📍 PASO 2: Verificar y reconfigurar PyQt5
echo ============================================================================

if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat

echo Verificando PyQt5 actual...
python -c "import PyQt5; print('PyQt5 versión:', PyQt5.Qt.QT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo ❌ PyQt5 con problemas, reinstalando...
    pip uninstall -y PyQt5 PyQt5-sip PyQt5-Qt5
    pip install PyQt5==5.15.9
) else (
    echo ✅ PyQt5 detectado
)

REM ============================================================================
echo.
echo 📍 PASO 3: Crear versión sin gráficos matplotlib
echo ============================================================================

echo Creando versión sin matplotlib para pruebas...

REM Crear script de prueba sin matplotlib
(
echo import sys
echo import os
echo.
echo # Configurar PyQt5 antes de importar
echo import os
echo os.environ['QT_QPA_PLATFORM'] = 'windows'
echo os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'
echo os.environ['QT_SCALE_FACTOR'] = '1'
echo.
echo try:
echo     from PyQt5.QtWidgets import QApplication, QMessageBox
echo     from PyQt5.QtCore import Qt
echo.
echo     print("🧪 Iniciando prueba básica de PyQt5..."^)
echo.
echo     app = QApplication(sys.argv^)
echo     
echo     # Configurar aplicación
echo     app.setAttribute(Qt.AA_EnableHighDpiScaling, False^)
echo     app.setAttribute(Qt.AA_UseHighDpiPixmaps, False^)
echo     
echo     # Crear ventana de prueba simple
echo     msg = QMessageBox(^)
echo     msg.setWindowTitle("Test PyQt5"^)
echo     msg.setText("✅ PyQt5 funciona correctamente!\n\nSi ves este mensaje, el problema está en matplotlib."^)
echo     msg.setStandardButtons(QMessageBox.Ok^)
echo     
echo     print("✅ Ventana de prueba creada"^)
echo     
echo     # Mostrar ventana
echo     result = msg.exec_^(^)
echo     
echo     print("✅ Prueba completada exitosamente"^)
echo     sys.exit(0^)
echo     
echo except Exception as e:
echo     print(f"❌ Error en PyQt5: {e}"^)
echo     input("Presiona Enter para continuar..."^)
echo     sys.exit(1^)
) > test_pyqt5_simple.py

echo ✅ Script de prueba creado: test_pyqt5_simple.py

echo.
echo 🧪 Ejecutando prueba básica de PyQt5...
python test_pyqt5_simple.py
set TEST_RESULT=%errorlevel%

if %TEST_RESULT% equ 0 (
    echo ✅ PyQt5 básico funciona - El problema está en matplotlib/gráficos
    goto MATPLOTLIB_SOLUTION
) else (
    echo ❌ PyQt5 básico falla - Problema más profundo
    goto DEEP_SOLUTION
)

:MATPLOTLIB_SOLUTION
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║           SOLUCIÓN: Problema con matplotlib             ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 📍 PASO 4: Configurar matplotlib para Windows
echo ============================================================================

echo Configurando matplotlib backend...
python -c "import matplotlib; matplotlib.use('Qt5Agg'); print('✅ Backend configurado')" 2>nul
if errorlevel 1 (
    echo ❌ matplotlib con problemas, reinstalando...
    pip uninstall -y matplotlib
    pip install matplotlib==3.5.3
)

echo Creando configuración matplotlib...
if not exist "%USERPROFILE%\.matplotlib" mkdir "%USERPROFILE%\.matplotlib"

(
echo backend: Qt5Agg
echo interactive: False
echo figure.max_open_warning: 0
) > "%USERPROFILE%\.matplotlib\matplotlibrc"

echo ✅ matplotlib configurado

REM Crear versión del main.py sin reportes gráficos
echo.
echo 📍 Creando versión sin gráficos avanzados...

(
echo @echo off
echo title Sistema POS - Modo Seguro ^(Sin Gráficos^)
echo.
echo echo ╔══════════════════════════════════════════════════════════╗
echo echo ║            SISTEMA POS - MODO SEGURO                    ║
echo echo ║              ^(Sin gráficos avanzados^)                    ║
echo echo ╚══════════════════════════════════════════════════════════╝
echo echo.
echo.
echo REM Configurar entorno
echo set QT_QPA_PLATFORM=windows
echo set QT_AUTO_SCREEN_SCALE_FACTOR=0
echo set QT_SCALE_FACTOR=1
echo set MPLBACKEND=Qt5Agg
echo.
echo if exist venv\Scripts\activate.bat call venv\Scripts\activate.bat
echo.
echo echo 🚀 Ejecutando Sistema POS en modo seguro...
echo echo 💡 Reportes gráficos deshabilitados temporalmente
echo echo.
echo.
echo python -c "import os; os.environ['DISABLE_MATPLOTLIB'] = '1'; exec(open('main.py').read())"
echo.
echo pause
) > run_pos_safe.bat

echo ✅ Creado: run_pos_safe.bat (modo sin gráficos)

goto TEST_SOLUTIONS

:DEEP_SOLUTION
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║         SOLUCIÓN PROFUNDA: Reinstalar PyQt5             ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 📍 PASO 4: Reinstalación completa de PyQt5
echo ============================================================================

echo 🗑️  Removiendo PyQt5 completamente...
pip uninstall -y PyQt5 PyQt5-sip PyQt5-Qt5 PyQt5-tools

echo 🧹 Limpiando cache de pip...
pip cache purge

echo 📦 Instalando PyQt5 versión estable específica...
pip install PyQt5==5.15.7

echo 📦 Instalando herramientas adicionales...
pip install PyQt5-tools==5.15.7.1.2

goto TEST_SOLUTIONS

:TEST_SOLUTIONS
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              PROBANDO SOLUCIONES                        ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🧪 Prueba 1: PyQt5 básico
python test_pyqt5_simple.py
if errorlevel 1 (
    echo ❌ PyQt5 básico aún falla
) else (
    echo ✅ PyQt5 básico funciona
)

echo.
echo 🧪 Prueba 2: Sistema en modo seguro
call run_pos_safe.bat
if errorlevel 1 (
    echo ❌ Modo seguro falla
) else (
    echo ✅ Modo seguro funciona
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    RESUMEN                              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 📋 Archivos creados:
echo    ✅ test_pyqt5_simple.py - Prueba básica de PyQt5
echo    ✅ run_pos_safe.bat - Sistema sin gráficos avanzados
echo    ✅ Configuración matplotlib mejorada
echo.

echo 💡 Opciones para ejecutar:
echo    1. run_pos_safe.bat - Sistema sin reportes gráficos
echo    2. test_pyqt5_simple.py - Probar solo PyQt5
echo    3. python main.py - Sistema completo (después de configuración)
echo.

echo 🔧 Si persisten problemas:
echo    - Reiniciar Windows
echo    - Verificar actualizaciones de drivers gráficos
echo    - Probar en modo compatibilidad
echo.

pause
