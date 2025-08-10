@echo off
chcp 65001 >nul
title Sistema POS - Inicio Rápido
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                 SISTEMA POS - INICIO RÁPIDO             ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Verificación básica
if not exist "main.py" (
    echo ❌ Error: No se encuentra en la carpeta del proyecto POS
    pause
    exit /b 1
)

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat >nul 2>&1
)

echo 🚀 Iniciando Sistema POS...
echo.
echo 👤 Credenciales:
echo    Admin: admin/admin123 | Cajero: cajero/cajero123
echo.

REM Ejecutar directamente
python main.py

echo.
echo 👋 Sistema POS cerrado
pause
