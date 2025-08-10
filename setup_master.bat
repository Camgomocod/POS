@echo off
chcp 65001 >nul
title Configuración Maestra - Sistema POS Windows 11
color 0F

echo ╔══════════════════════════════════════════════════════════╗
echo ║              CONFIGURACIÓN MAESTRA                      ║
echo ║                Sistema POS v1.0                         ║
echo ║              Windows 11 - Setup Complete               ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🎯 Este script configurará completamente el Sistema POS en Windows 11
echo.

REM Verificar ubicación
if not exist "main.py" (
    echo ❌ Error: No se encuentra main.py
    echo 💡 Ejecuta este script desde la carpeta del proyecto POS
    pause
    exit /b 1
)

echo ✅ Ubicado en carpeta del proyecto correcta
echo 📁 %CD%
echo.

:MENU_PRINCIPAL
cls
echo ╔══════════════════════════════════════════════════════════╗
echo ║              CONFIGURACIÓN MAESTRA - SISTEMA POS        ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🛠️  Selecciona la configuración que deseas realizar:
echo.
echo [1] 🔍 Verificar requisitos del sistema
echo [2] 🚀 Instalación completa (Recomendado para primera vez)
echo [3] 🔗 Crear accesos directos únicamente
echo [4] 🔧 Configurar permisos y políticas
echo [5] ⚡ Instalación rápida (sin verificaciones extensas)
echo [6] 🧪 Probar sistema (después de instalación)
echo [7] 📋 Mostrar información del proyecto
echo [8] 🆘 Reparar instalación existente
echo [9] 🚪 Salir
echo.
set /p choice="Selecciona una opción (1-9): "

if "%choice%"=="1" goto CHECK_REQUIREMENTS
if "%choice%"=="2" goto FULL_INSTALL
if "%choice%"=="3" goto CREATE_SHORTCUTS
if "%choice%"=="4" goto SETUP_PERMISSIONS
if "%choice%"=="5" goto QUICK_INSTALL
if "%choice%"=="6" goto TEST_SYSTEM
if "%choice%"=="7" goto SHOW_INFO
if "%choice%"=="8" goto REPAIR_INSTALL
if "%choice%"=="9" goto EXIT

echo ❌ Opción no válida
timeout /t 2 >nul
goto MENU_PRINCIPAL

:CHECK_REQUIREMENTS
cls
echo 🔍 Verificando requisitos del sistema...
call check_requirements.bat
pause
goto MENU_PRINCIPAL

:FULL_INSTALL
cls
echo 🚀 Iniciando instalación completa...
echo.
echo 📋 Pasos a realizar:
echo    1. Verificar requisitos
echo    2. Crear entorno virtual
echo    3. Instalar dependencias
echo    4. Crear accesos directos
echo    5. Configurar permisos
echo    6. Probar sistema
echo.
set /p confirm="¿Continuar con la instalación completa? (s/n): "
if /i not "%confirm%"=="s" goto MENU_PRINCIPAL

echo.
echo 📍 Paso 1/6: Verificando requisitos...
call check_requirements.bat

echo.
echo 📍 Paso 2-3/6: Instalando sistema...
call install_pos_w11.bat

echo.
echo 📍 Paso 4/6: Creando accesos directos...
PowerShell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1

echo.
echo 📍 Paso 5/6: Configurando permisos...
call setup_permissions.bat

echo.
echo 📍 Paso 6/6: Probando sistema...
echo ¿Deseas probar el sistema ahora?
set /p test="(s/n): "
if /i "%test%"=="s" call quick_start.bat

echo.
echo ✅ ¡Instalación completa terminada!
pause
goto MENU_PRINCIPAL

:CREATE_SHORTCUTS
cls
echo 🔗 Creando accesos directos...
PowerShell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1
pause
goto MENU_PRINCIPAL

:SETUP_PERMISSIONS
cls
echo 🔧 Configurando permisos...
call setup_permissions.bat
pause
goto MENU_PRINCIPAL

:QUICK_INSTALL
cls
echo ⚡ Instalación rápida...
call install_pos_w11.bat
echo.
echo ✅ Instalación rápida completada
pause
goto MENU_PRINCIPAL

:TEST_SYSTEM
cls
echo 🧪 Probando sistema...
echo.
echo Selecciona el tipo de prueba:
echo [1] 🚀 Inicio rápido
echo [2] 🔍 Inicio con verificaciones
echo [3] 🗄️  Verificar solo base de datos
echo.
set /p test_choice="Opción (1-3): "

if "%test_choice%"=="1" (
    call quick_start.bat
) else if "%test_choice%"=="2" (
    call run_pos.bat
) else if "%test_choice%"=="3" (
    if exist "verify_clean_database.py" (
        python verify_clean_database.py
    ) else (
        echo ❌ Script de verificación no encontrado
    )
    pause
) else (
    echo ❌ Opción no válida
    pause
)
goto MENU_PRINCIPAL

:SHOW_INFO
cls
echo ╔══════════════════════════════════════════════════════════╗
echo ║                INFORMACIÓN DEL PROYECTO                 ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 📁 Carpeta del proyecto: %CD%
echo 📅 Fecha: %DATE% %TIME%
echo.

echo 📋 Archivos de configuración disponibles:
if exist "install_pos_w11.bat" echo ✅ install_pos_w11.bat - Instalador principal
if exist "run_pos.bat" echo ✅ run_pos.bat - Ejecutor del sistema
if exist "quick_start.bat" echo ✅ quick_start.bat - Inicio rápido
if exist "check_requirements.bat" echo ✅ check_requirements.bat - Verificador
if exist "setup_permissions.bat" echo ✅ setup_permissions.bat - Permisos
if exist "create_desktop_shortcut.ps1" echo ✅ create_desktop_shortcut.ps1 - Accesos directos

echo.
echo 📊 Estado del entorno:
if exist "venv" (
    echo ✅ Entorno virtual: Configurado
) else (
    echo ❌ Entorno virtual: No configurado
)

if exist "data\pos.db" (
    for %%A in ("data\pos.db") do echo ✅ Base de datos: %%~zA bytes
) else (
    echo ❌ Base de datos: No encontrada
)

echo.
echo 👤 Credenciales por defecto:
echo    Admin: admin / admin123
echo    Cajero: cajero / cajero123
echo.

if exist "README_WINDOWS.md" (
    echo 📖 Para más información, revisar: README_WINDOWS.md
)

echo.
pause
goto MENU_PRINCIPAL

:REPAIR_INSTALL
cls
echo 🆘 Reparando instalación...
echo.
echo ⚠️  Esta opción eliminará el entorno virtual actual y reinstalará
set /p confirm_repair="¿Continuar con la reparación? (s/n): "
if /i not "%confirm_repair%"=="s" goto MENU_PRINCIPAL

echo.
echo 🗑️  Eliminando entorno virtual anterior...
if exist "venv" rmdir /s /q venv

echo 🔄 Ejecutando instalación limpia...
call install_pos_w11.bat

echo ✅ Reparación completada
pause
goto MENU_PRINCIPAL

:EXIT
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    ¡CONFIGURACIÓN LISTA!                ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 🎯 El Sistema POS está configurado y listo para usar
echo.
echo 📋 Formas de ejecutar:
echo    • Acceso directo en escritorio: "Sistema POS"
echo    • Desde esta carpeta: run_pos.bat
echo    • Inicio rápido: quick_start.bat
echo.
echo 👤 Credenciales iniciales:
echo    Admin: admin/admin123 | Cajero: cajero/cajero123
echo.
echo 📖 Documentación completa en: README_WINDOWS.md
echo.
echo 👋 ¡Gracias por usar el Sistema POS!
pause
exit /b 0
