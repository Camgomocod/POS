@echo off
title Sistema POS - Instalacion de Emergencia
color 0A

echo ================================================================
echo                SISTEMA POS - INSTALACION SIMPLE
echo ================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo Instalar Python desde python.org
    pause
    exit /b 1
)

echo Python OK

REM Crear entorno virtual
if exist venv rmdir /s /q venv
python -m venv venv
call venv\Scripts\activate.bat

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ================================================================
echo                    INSTALACION COMPLETADA
echo ================================================================
echo.
echo Para ejecutar: run_pos.bat
echo Credenciales: admin/admin123 y cajero/cajero123
echo.
pause
