@echo off
chcp 65001 >nul
title Crear Acceso Directo - Sistema POS
color 0C

echo ╔══════════════════════════════════════════════════════════╗
echo ║              CREAR ACCESO DIRECTO                        ║
echo ║                Sistema POS v1.0                         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Obtener directorio actual
set PROJECT_DIR=%~dp0
echo 📁 Directorio del proyecto: %PROJECT_DIR%

REM Verificar que estamos en la carpeta correcta
if not exist "main.py" (
    echo ❌ Error: No se encuentra main.py
    echo 💡 Asegúrate de ejecutar este script desde la carpeta del proyecto POS
    pause
    exit /b 1
)

echo ✅ Proyecto POS detectado correctamente
echo.

REM Método 1: Usar VBS para crear acceso directo
echo 🔗 Creando acceso directo usando VBScript...

REM Crear script VBS temporal
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo DesktopPath = WshShell.SpecialFolders^("Desktop"^)
echo Set oShellLink = WshShell.CreateShortcut^(DesktopPath ^& "\Sistema POS.lnk"^)
echo oShellLink.TargetPath = "cmd.exe"
echo oShellLink.Arguments = "/k ""cd /d ""%PROJECT_DIR%"" && run_pos.bat"""
echo oShellLink.WorkingDirectory = "%PROJECT_DIR%"
echo oShellLink.Description = "Sistema POS - Restaurante Fast"
echo oShellLink.Save
echo WScript.Echo "Acceso directo creado exitosamente"
) > temp_shortcut.vbs

REM Ejecutar script VBS
cscript //nologo temp_shortcut.vbs 2>nul
if errorlevel 1 (
    echo ⚠️  Método VBS falló, intentando método manual...
    goto MANUAL_SHORTCUT
) else (
    echo ✅ Acceso directo principal creado: Sistema POS.lnk
)

REM Crear acceso directo para inicio rápido
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo DesktopPath = WshShell.SpecialFolders^("Desktop"^)
echo Set oShellLink = WshShell.CreateShortcut^(DesktopPath ^& "\Sistema POS - Inicio Rapido.lnk"^)
echo oShellLink.TargetPath = "cmd.exe"
echo oShellLink.Arguments = "/k ""cd /d ""%PROJECT_DIR%"" && quick_start.bat"""
echo oShellLink.WorkingDirectory = "%PROJECT_DIR%"
echo oShellLink.Description = "Sistema POS - Inicio Rápido"
echo oShellLink.Save
) > temp_shortcut_quick.vbs

cscript //nologo temp_shortcut_quick.vbs 2>nul
if not errorlevel 1 (
    echo ✅ Acceso directo rápido creado: Sistema POS - Inicio Rapido.lnk
)

REM Limpiar archivos temporales
del temp_shortcut.vbs 2>nul
del temp_shortcut_quick.vbs 2>nul

goto SUCCESS

:MANUAL_SHORTCUT
echo.
echo 📋 INSTRUCCIONES PARA CREAR ACCESO DIRECTO MANUALMENTE:
echo.
echo 1. Clic derecho en el escritorio
echo 2. Nuevo → Acceso directo
echo 3. En "Ubicación del elemento" escribir:
echo    cmd.exe /k "cd /d "%PROJECT_DIR%" && run_pos.bat"
echo.
echo 4. Siguiente
echo 5. Nombre: Sistema POS
echo 6. Finalizar
echo.

:SUCCESS
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              ✅ PROCESO COMPLETADO                       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

if exist "%USERPROFILE%\Desktop\Sistema POS.lnk" (
    echo 🎯 Accesos directos creados en el escritorio:
    echo    ✅ Sistema POS.lnk - Ejecución normal
    if exist "%USERPROFILE%\Desktop\Sistema POS - Inicio Rapido.lnk" (
        echo    ✅ Sistema POS - Inicio Rapido.lnk - Inicio rápido
    )
    echo.
    echo 💡 Para usar:
    echo    - Doble clic en cualquiera de los accesos directos
    echo    - O ejecutar run_pos.bat desde esta carpeta
) else (
    echo ⚠️  No se detectaron accesos directos automáticos
    echo 💡 Usa las instrucciones manuales mostradas arriba
    echo 💡 O ejecuta directamente: run_pos.bat
)

echo.
echo 👤 Credenciales del sistema:
echo    Admin: admin / admin123
echo    Cajero: cajero / cajero123
echo.

set /p test_now="¿Deseas probar el sistema ahora? (s/n): "
if /i "%test_now%"=="s" (
    echo.
    echo 🚀 Iniciando Sistema POS...
    call run_pos.bat
)

echo.
pause
