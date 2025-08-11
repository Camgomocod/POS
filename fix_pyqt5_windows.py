#!/usr/bin/env python3
"""
Solución específica para el problema de PyQt5 en Windows 11
Ejecutar cuando PyQt5 está instalado pero la aplicación no lo encuentra
"""

import sys
import os
import subprocess
from pathlib import Path

def print_status(message, is_success=True):
    """Imprimir mensaje con estado"""
    prefix = "✅" if is_success else "❌"
    print(f"{prefix} {message}")

def check_python_installation():
    """Verificar instalación de Python"""
    print("🔍 VERIFICANDO INSTALACIÓN DE PYTHON")
    print("=" * 40)
    
    # Información básica
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path}")
    
    # Verificar si está usando Python del Microsoft Store
    if "WindowsApps" in sys.executable or "Microsoft" in sys.executable:
        print("⚠️  DETECTADO: Python del Microsoft Store")
        print("   Esto puede causar problemas con rutas de paquetes")
        return "store"
    else:
        print("✅ Python estándar detectado")
        return "standard"

def check_package_locations():
    """Verificar ubicaciones de paquetes"""
    print("\n🔍 VERIFICANDO UBICACIONES DE PAQUETES")
    print("=" * 42)
    
    # Verificar where PyQt5 está instalado
    try:
        import PyQt5
        print(f"PyQt5 location: {PyQt5.__file__}")
        print_status("PyQt5 importable", True)
    except ImportError as e:
        print_status(f"PyQt5 no importable: {e}", False)
        return False
    
    # Verificar site-packages
    import site
    print(f"Site packages: {site.getsitepackages()}")
    print(f"User site packages: {site.getusersitepackages()}")
    
    return True

def fix_python_path():
    """Intentar corregir el PYTHONPATH"""
    print("\n🔧 CORRIGIENDO PYTHON PATH")
    print("=" * 30)
    
    try:
        import site
        user_site = site.getusersitepackages()
        
        if user_site not in sys.path:
            sys.path.insert(0, user_site)
            print_status(f"Agregado user site al path: {user_site}")
        
        # Verificar si ahora PyQt5 funciona
        try:
            from PyQt5.QtWidgets import QApplication
            print_status("PyQt5 ahora funciona correctamente")
            return True
        except ImportError:
            print_status("PyQt5 aún no funciona", False)
            return False
            
    except Exception as e:
        print_status(f"Error al corregir path: {e}", False)
        return False

def create_environment_fix():
    """Crear script para configurar entorno"""
    print("\n🔧 CREANDO SCRIPT DE CONFIGURACIÓN")
    print("=" * 35)
    
    # Script batch para Windows
    batch_content = '''@echo off
echo "🔧 Configurando entorno para POS en Windows 11"

:: Configurar variables de entorno para Qt
set QT_QPA_PLATFORM=windows
set QT_AUTO_SCREEN_SCALE_FACTOR=1

:: Agregar user site-packages al PYTHONPATH
for /f "tokens=*" %%i in ('python -c "import site; print(site.getusersitepackages())"') do set USER_SITE=%%i
set PYTHONPATH=%USER_SITE%;%PYTHONPATH%

echo "✅ Variables configuradas:"
echo "   QT_QPA_PLATFORM: %QT_QPA_PLATFORM%"
echo "   QT_AUTO_SCREEN_SCALE_FACTOR: %QT_AUTO_SCREEN_SCALE_FACTOR%"
echo "   USER_SITE: %USER_SITE%"

echo.
echo "🚀 Ejecutando aplicación POS..."
python main.py

pause
'''
    
    try:
        with open("run_pos_fixed.bat", "w", encoding="utf-8") as f:
            f.write(batch_content)
        print_status("Script run_pos_fixed.bat creado")
        
        # Script PowerShell también
        ps_content = '''# Configuración de entorno para POS
Write-Host "🔧 Configurando entorno para POS en Windows 11" -ForegroundColor Cyan

# Configurar variables Qt
$env:QT_QPA_PLATFORM = "windows"
$env:QT_AUTO_SCREEN_SCALE_FACTOR = "1"

# Obtener user site-packages
$userSite = python -c "import site; print(site.getusersitepackages())"
$env:PYTHONPATH = "$userSite;$env:PYTHONPATH"

Write-Host "✅ Variables configuradas:" -ForegroundColor Green
Write-Host "   QT_QPA_PLATFORM: $env:QT_QPA_PLATFORM"
Write-Host "   QT_AUTO_SCREEN_SCALE_FACTOR: $env:QT_AUTO_SCREEN_SCALE_FACTOR" 
Write-Host "   USER_SITE: $userSite"

Write-Host "`n🚀 Ejecutando aplicación POS..." -ForegroundColor Green
python main.py

Read-Host "`nPresiona Enter para salir"
'''
        
        with open("run_pos_fixed.ps1", "w", encoding="utf-8") as f:
            f.write(ps_content)
        print_status("Script run_pos_fixed.ps1 creado")
        
        return True
        
    except Exception as e:
        print_status(f"Error al crear scripts: {e}", False)
        return False

def test_application():
    """Probar la aplicación con el entorno corregido"""
    print("\n🧪 PROBANDO APLICACIÓN CON ENTORNO CORREGIDO")
    print("=" * 45)
    
    # Configurar entorno
    os.environ['QT_QPA_PLATFORM'] = 'windows'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    
    # Agregar user site al path
    try:
        import site
        user_site = site.getusersitepackages()
        if user_site not in sys.path:
            sys.path.insert(0, user_site)
    except:
        pass
    
    try:
        # Verificar importaciones críticas
        from PyQt5.QtWidgets import QApplication
        print_status("PyQt5.QtWidgets importado")
        
        from PyQt5.QtCore import Qt, QCoreApplication
        print_status("PyQt5.QtCore importado")
        
        # Crear aplicación de prueba
        app = QApplication([])
        print_status("QApplication creada exitosamente")
        
        app.quit()
        print_status("Test de aplicación completado exitosamente")
        
        return True
        
    except Exception as e:
        print_status(f"Error en test de aplicación: {e}", False)
        return False

def main():
    """Función principal"""
    print("🔧 SOLUCIONADOR DE PROBLEMAS PYQT5 - WINDOWS 11")
    print("=" * 50)
    
    # 1. Verificar instalación de Python
    python_type = check_python_installation()
    
    # 2. Verificar ubicaciones de paquetes
    packages_ok = check_package_locations()
    
    if not packages_ok:
        print("\n❌ No se pudo verificar PyQt5. Reinstalar:")
        print("   pip uninstall PyQt5 -y")
        print("   pip install PyQt5==5.15.9")
        return
    
    # 3. Intentar corregir el path
    path_fixed = fix_python_path()
    
    # 4. Crear scripts de configuración
    scripts_created = create_environment_fix()
    
    # 5. Probar aplicación
    app_works = test_application()
    
    # Resumen y recomendaciones
    print("\n📋 RESUMEN Y RECOMENDACIONES")
    print("=" * 30)
    
    if app_works:
        print("🎉 ¡PROBLEMA RESUELTO!")
        print("\n📌 Para usar la aplicación, ejecutar:")
        print("   run_pos_fixed.bat")
        print("   O en PowerShell: .\\run_pos_fixed.ps1")
        
    else:
        print("⚠️  PROBLEMA PERSISTENTE")
        print("\n📌 Soluciones recomendadas:")
        
        if python_type == "store":
            print("1. INSTALAR PYTHON ESTÁNDAR desde python.org")
            print("   (Recomendado para evitar problemas con Microsoft Store)")
        
        print("2. CREAR ENTORNO VIRTUAL:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate")
        print("   pip install -r requirements.txt")
        
        print("3. USAR CONDA (alternativa):")
        print("   conda create -n pos_env python=3.9")
        print("   conda activate pos_env")
        print("   conda install pyqt=5.15.9")
    
    print("\n✅ Diagnóstico completado")

if __name__ == "__main__":
    main()
