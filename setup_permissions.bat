@echo off
chcp 65001 >nul
title Configuración de Permisos - Sistema POS
color 0D

echo ╔══════════════════════════════════════════════════════════╗
echo ║             CONFIGURACIÓN DE PERMISOS                   ║
echo ║                   Sistema POS v1.0                      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Ejecutándose con permisos de administrador
) else (
    echo ⚠️  No se detectaron permisos de administrador
    echo 💡 Para configurar permisos completos, ejecutar como administrador
    echo.
)

echo 🔧 Configurando permisos para el Sistema POS...
echo.

REM Configurar permisos de ejecución para scripts
echo 📍 Configurando permisos de scripts...
if exist "*.bat" (
    attrib -r *.bat
    echo ✅ Permisos de lectura/escritura configurados para archivos .bat
)

if exist "*.ps1" (
    attrib -r *.ps1
    echo ✅ Permisos configurados para archivos PowerShell
)

REM Configurar permisos para carpetas
echo.
echo 📍 Configurando permisos de carpetas...

REM Carpeta data
if exist "data" (
    attrib -r data\*.* /s
    echo ✅ Permisos configurados para carpeta data\
) else (
    mkdir data
    echo ✅ Carpeta data\ creada
)

REM Carpeta venv
if exist "venv" (
    attrib -r venv\*.* /s
    echo ✅ Permisos configurados para entorno virtual
)

REM Configurar PowerShell ExecutionPolicy para usuario actual
echo.
echo 📍 Configurando política de ejecución de PowerShell...

powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" 2>nul
if errorlevel 1 (
    echo ⚠️  No se pudo configurar automáticamente PowerShell ExecutionPolicy
    echo 💡 Ejecuta manualmente: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
) else (
    echo ✅ PowerShell ExecutionPolicy configurado para usuario actual
)

REM Configurar exclusiones de Windows Defender si es posible
echo.
echo 📍 Configurando exclusiones de Windows Defender...

set PROJECT_DIR=%~dp0

REM Intentar agregar exclusión (requiere permisos de admin)
powershell -Command "Add-MpPreference -ExclusionPath '%PROJECT_DIR%'" 2>nul
if errorlevel 1 (
    echo ⚠️  No se pudo agregar exclusión automáticamente a Windows Defender
    echo 💡 Para mejor rendimiento, agregar manualmente:
    echo    - Abrir Windows Security
    echo    - Virus y threat protection
    echo    - Exclusions
    echo    - Agregar: %PROJECT_DIR%
) else (
    echo ✅ Carpeta del proyecto agregada a exclusiones de Windows Defender
)

REM Configurar firewall si es necesario
echo.
echo 📍 Verificando configuración de firewall...
echo ℹ️  El Sistema POS no requiere configuración especial de firewall
echo ℹ️  Solo usa conexiones locales y archivos del sistema

REM Crear script de permisos para emergencias
echo.
echo 📍 Creando script de reparación de permisos...

echo @echo off > fix_permissions.bat
echo echo Reparando permisos... >> fix_permissions.bat
echo icacls . /grant Users:F /T >> fix_permissions.bat
echo attrib -r *.* /s >> fix_permissions.bat
echo echo Permisos reparados >> fix_permissions.bat
echo pause >> fix_permissions.bat

echo ✅ Script de reparación creado: fix_permissions.bat

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              ✅ CONFIGURACIÓN COMPLETADA                 ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🎯 Configuraciones aplicadas:
echo    ✅ Permisos de archivos de script
echo    ✅ Permisos de carpetas del proyecto
echo    ✅ PowerShell ExecutionPolicy
echo    ✅ Script de reparación de emergencia
echo.

net session >nul 2>&1
if %errorLevel% equ 0 (
    echo 🔒 Configuraciones con permisos de administrador aplicadas
) else (
    echo ⚠️  Algunas configuraciones requieren permisos de administrador
    echo 💡 Para configuración completa, ejecutar como administrador
)

echo.
echo 📋 Si tienes problemas de permisos:
echo    1. Ejecutar fix_permissions.bat como administrador
echo    2. Verificar exclusiones de antivirus
echo    3. Revisar permisos de la carpeta del proyecto
echo.

pause
