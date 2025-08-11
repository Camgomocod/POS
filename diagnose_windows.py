#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de ejecución en Windows 11
Ejecutar este script para identificar problemas potenciales
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def print_header(title):
    """Imprimir encabezado de sección"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_result(test_name, result, details=""):
    """Imprimir resultado de test"""
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"   📝 {details}")

def check_python_version():
    """Verificar versión de Python"""
    print_header("VERIFICACIÓN DE PYTHON")
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Platform: {platform.platform()}")
    
    # Python debe ser 3.7+
    is_valid = version.major == 3 and version.minor >= 7
    print_result("Python 3.7+", is_valid, f"Actual: {version.major}.{version.minor}")
    
    return is_valid

def check_required_packages():
    """Verificar paquetes requeridos"""
    print_header("VERIFICACIÓN DE PAQUETES")
    
    required_packages = [
        'PyQt5',
        'sqlalchemy', 
        'pandas',
        'numpy',
        'matplotlib',
        'openpyxl'
    ]
    
    # En Windows también verificar pywin32
    if platform.system() == "Windows":
        required_packages.append('pywin32')
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print_result(f"Package {package}", True)
        except ImportError as e:
            print_result(f"Package {package}", False, str(e))
            all_installed = False
    
    return all_installed

def check_pyqt5_specifics():
    """Verificar específicos de PyQt5"""
    print_header("VERIFICACIÓN DE PyQt5")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt, QCoreApplication
        from PyQt5.QtGui import QFont, QIcon
        print_result("PyQt5 import", True)
        
        # Verificar si se puede crear una QApplication (problema común en Windows)
        try:
            # Verificar si ya hay una aplicación corriendo
            existing_app = QApplication.instance()
            if existing_app is None:
                test_app = QApplication([])
                print_result("QApplication creation", True)
                test_app.quit()
            else:
                print_result("QApplication creation", True, "Ya existe una instancia")
                
        except Exception as e:
            print_result("QApplication creation", False, str(e))
            return False
            
    except ImportError as e:
        print_result("PyQt5 import", False, str(e))
        return False
    
    return True

def check_file_permissions():
    """Verificar permisos de archivos"""
    print_header("VERIFICACIÓN DE PERMISOS")
    
    project_root = Path(__file__).parent
    
    # Verificar si podemos leer archivos principales
    key_files = [
        'main.py',
        'config.py', 
        'requirements.txt',
        'data/pos.db'
    ]
    
    all_accessible = True
    
    for file_name in key_files:
        file_path = project_root / file_name
        
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    f.read(100)  # Leer primeros 100 caracteres
                print_result(f"Read access: {file_name}", True)
            except Exception as e:
                print_result(f"Read access: {file_name}", False, str(e))
                all_accessible = False
        else:
            print_result(f"File exists: {file_name}", False, "Archivo no encontrado")
            all_accessible = False
    
    return all_accessible

def check_database():
    """Verificar base de datos"""
    print_header("VERIFICACIÓN DE BASE DE DATOS")
    
    try:
        # Intentar importar e inicializar la base de datos
        sys.path.append(str(Path(__file__).parent))
        from utils.database import init_database
        from models.base import get_db
        
        # Intentar inicializar
        init_database()
        print_result("Database initialization", True)
        
        # Verificar conexión
        db = get_db()
        db.close()
        print_result("Database connection", True)
        
        return True
        
    except Exception as e:
        print_result("Database check", False, str(e))
        return False

def check_windows_specifics():
    """Verificaciones específicas de Windows"""
    print_header("VERIFICACIONES ESPECÍFICAS DE WINDOWS")
    
    if platform.system() != "Windows":
        print("ℹ️  No se ejecuta en Windows, omitiendo verificaciones específicas")
        return True
    
    # Verificar variables de entorno importantes
    env_vars = ['PATH', 'PYTHONPATH', 'QT_QPA_PLATFORM_PLUGIN_PATH']
    
    for var in env_vars:
        value = os.environ.get(var, "")
        if value:
            print_result(f"Environment variable {var}", True, f"Set ({len(value)} chars)")
        else:
            print_result(f"Environment variable {var}", False, "Not set")
    
    # Verificar si Visual C++ Redistributable está instalado (requerido por PyQt5)
    try:
        import ctypes
        try:
            ctypes.cdll.msvcr140  # VC++ 2015-2019
            print_result("Visual C++ Redistributable", True)
        except OSError:
            print_result("Visual C++ Redistributable", False, "Puede requerirse instalación")
    except:
        print_result("Visual C++ check", False, "No se pudo verificar")
    
    return True

def run_minimal_test():
    """Ejecutar un test mínimo de la aplicación"""
    print_header("TEST MÍNIMO DE APLICACIÓN")
    
    try:
        # Agregar directorio actual al path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # Intentar importar controladores principales
        from controllers.app_controller import AppController
        print_result("Import AppController", True)
        
        from views.login_window import LoginWindow  
        print_result("Import LoginWindow", True)
        
        # Intentar crear una aplicación QT mínima
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QTimer
        
        # Verificar si ya existe una app
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
            app_created = True
        else:
            app_created = False
            
        print_result("QApplication ready", True)
        
        # Intentar crear ventana de login (sin mostrar)
        try:
            login_window = LoginWindow()
            print_result("LoginWindow creation", True)
            
            # Limpiar
            login_window.deleteLater()
            
        except Exception as e:
            print_result("LoginWindow creation", False, str(e))
            return False
        
        # Limpiar aplicación si la creamos
        if app_created:
            app.quit()
            
        return True
        
    except Exception as e:
        print_result("Minimal app test", False, str(e))
        import traceback
        print(f"📋 Traceback:\n{traceback.format_exc()}")
        return False

def generate_windows_fix_script():
    """Generar script de solución para Windows"""
    print_header("GENERANDO SCRIPT DE SOLUCIÓN")
    
    fix_script = """@echo off
echo "🔧 Script de reparación para POS en Windows 11"
echo.

echo "📦 Reinstalando PyQt5..."
pip uninstall PyQt5 -y
pip install PyQt5==5.15.9

echo.
echo "📦 Reinstalando dependencias..."
pip install -r requirements.txt --force-reinstall

echo.
echo "🔧 Configurando variables de entorno..."
set QT_QPA_PLATFORM=windows
set QT_AUTO_SCREEN_SCALE_FACTOR=1

echo.
echo "▶️  Intentando ejecutar aplicación..."
python main.py

echo.
echo "✅ Script completado. Si persisten problemas:"
echo "   1. Instalar Visual C++ Redistributable 2015-2019"
echo "   2. Ejecutar como administrador"
echo "   3. Verificar antivirus no bloquee Python"
pause
"""
    
    try:
        with open("fix_windows.bat", "w", encoding="utf-8") as f:
            f.write(fix_script)
        print_result("Script fix_windows.bat generado", True)
    except Exception as e:
        print_result("Generación de script", False, str(e))

def main():
    """Función principal de diagnóstico"""
    print("🏥 DIAGNÓSTICO DE POS EN WINDOWS 11")
    print("===================================")
    
    # Lista de verificaciones
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages), 
        ("PyQt5 Specifics", check_pyqt5_specifics),
        ("File Permissions", check_file_permissions),
        ("Database", check_database),
        ("Windows Specifics", check_windows_specifics),
        ("Minimal App Test", run_minimal_test)
    ]
    
    results = {}
    
    # Ejecutar todas las verificaciones
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ Error en {check_name}: {e}")
            results[check_name] = False
    
    # Resumen final
    print_header("RESUMEN DE DIAGNÓSTICO")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"✅ Verificaciones pasadas: {passed}/{total}")
    
    if passed == total:
        print("🎉 Todas las verificaciones pasaron. El problema puede ser:")
        print("   • Conflicto con antivirus")
        print("   • Permisos de Windows")
        print("   • Otra aplicación usando PyQt5")
    else:
        print("⚠️  Se encontraron problemas. Recomendaciones:")
        failed_checks = [name for name, result in results.items() if not result]
        for check in failed_checks:
            print(f"   • Resolver problema en: {check}")
    
    # Generar script de solución
    generate_windows_fix_script()
    
    print("\n📋 PASOS SUGERIDOS PARA WINDOWS 11:")
    print("1. Ejecutar fix_windows.bat como administrador")
    print("2. Desactivar antivirus temporalmente")
    print("3. Instalar Visual C++ Redistributable si falta")
    print("4. Ejecutar: python diagnose_windows.py")
    print("5. Si persiste, ejecutar: python main.py --debug")

if __name__ == "__main__":
    main()
