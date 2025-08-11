#!/usr/bin/env python3
"""
Script de verificación para instalación Windows 11
Comprueba que todo esté configurado correctamente para el testing
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Windows11Validator:
    """Validador de instalación para Windows 11"""
    
    def __init__(self):
        self.project_path = Path(__file__).parent.absolute()
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
    
    def check_item(self, description, condition, error_msg=None, warning_msg=None):
        """Verificar un elemento y registrar resultado"""
        self.total_checks += 1
        print(f"🔍 {description}...", end=" ")
        
        if condition:
            print("✅")
            self.success_count += 1
            return True
        else:
            if error_msg:
                print("❌")
                self.errors.append(f"❌ {description}: {error_msg}")
            elif warning_msg:
                print("⚠️ ")
                self.warnings.append(f"⚠️ {description}: {warning_msg}")
            else:
                print("❌")
                self.errors.append(f"❌ {description}")
            return False
    
    def check_python_installation(self):
        """Verificar instalación de Python"""
        print("\n🐍 VERIFICANDO PYTHON:")
        print("─" * 40)
        
        python_commands = ["py", "python", "python3"]
        python_found = False
        python_version = None
        
        for cmd in python_commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    python_version = result.stdout.strip()
                    self.check_item(f"Python disponible ({cmd})", True)
                    python_found = True
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        self.check_item("Python instalado", python_found, 
                       "Python no encontrado. Instalar desde python.org")
        
        if python_found:
            # Verificar versión
            version_ok = "3.1" in python_version or "3.9" in python_version or "3.8" in python_version
            self.check_item(f"Versión Python válida ({python_version})", version_ok,
                           "Se recomienda Python 3.8+")
        
        return python_found
    
    def check_dependencies(self):
        """Verificar dependencias de Python"""
        print("\n📦 VERIFICANDO DEPENDENCIAS:")
        print("─" * 40)
        
        required_packages = [
            ("PyQt5", "PyQt5"),
            ("SQLAlchemy", "sqlalchemy"),
            ("Faker", "faker"),
        ]
        
        windows_packages = [
            ("winshell", "winshell"),
            ("pywin32", "win32com.client"),
        ]
        
        all_packages = required_packages + (windows_packages if platform.system() == "Windows" else [])
        
        for package_name, import_name in all_packages:
            try:
                __import__(import_name)
                self.check_item(f"Paquete {package_name}", True)
            except ImportError:
                self.check_item(f"Paquete {package_name}", False,
                               f"Instalar con: pip install {package_name}")
    
    def check_project_files(self):
        """Verificar archivos del proyecto"""
        print("\n📁 VERIFICANDO ARCHIVOS DEL PROYECTO:")
        print("─" * 40)
        
        essential_files = [
            ("main.py", "Archivo principal de la aplicación"),
            ("config.py", "Archivo de configuración"),
            ("requirements.txt", "Lista de dependencias"),
        ]
        
        for filename, description in essential_files:
            file_path = self.project_path / filename
            self.check_item(f"{description} ({filename})", file_path.exists(),
                           f"Archivo {filename} no encontrado")
        
        # Verificar directorios
        essential_dirs = [
            ("controllers", "Controladores de la aplicación"),
            ("models", "Modelos de datos"),
            ("views", "Interfaces de usuario"),
            ("utils", "Utilidades"),
            ("data", "Base de datos"),
        ]
        
        for dirname, description in essential_dirs:
            dir_path = self.project_path / dirname
            self.check_item(f"{description} (/{dirname})", dir_path.exists(),
                           f"Directorio {dirname} no encontrado")
    
    def check_database(self):
        """Verificar base de datos"""
        print("\n💾 VERIFICANDO BASE DE DATOS:")
        print("─" * 40)
        
        db_path = self.project_path / "data" / "pos.db"
        self.check_item("Base de datos existe", db_path.exists(),
                       "Base de datos no encontrada. Ejecutar create_minimal_db.py")
        
        if db_path.exists():
            db_size = db_path.stat().st_size
            self.check_item(f"Tamaño de base de datos ({db_size} bytes)", db_size > 1000,
                           "Base de datos muy pequeña, posiblemente corrupta")
    
    def check_launcher_files(self):
        """Verificar archivos de lanzamiento"""
        print("\n🚀 VERIFICANDO LAUNCHERS:")
        print("─" * 40)
        
        launcher_files = [
            ("POS_Windows11.bat", "Launcher avanzado para Windows 11"),
            ("POS_RestauranteFast.bat", "Launcher simple"),
            ("create_shortcuts.py", "Script creador de accesos directos"),
            ("install_windows11.ps1", "Instalador PowerShell"),
        ]
        
        for filename, description in launcher_files:
            file_path = self.project_path / filename
            self.check_item(f"{description} ({filename})", file_path.exists(),
                           f"Archivo {filename} no encontrado")
    
    def check_shortcuts(self):
        """Verificar accesos directos (solo Windows)"""
        if platform.system() != "Windows":
            print("\n🔗 ACCESOS DIRECTOS:")
            print("─" * 40)
            print("⏭️  Saltando verificación de accesos directos (no Windows)")
            return
        
        print("\n🔗 VERIFICANDO ACCESOS DIRECTOS:")
        print("─" * 40)
        
        try:
            import winshell
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "POS RestauranteFast.lnk")
            self.check_item("Acceso directo en escritorio", os.path.exists(shortcut_path),
                           "Ejecutar create_shortcuts.py o install_windows11.ps1")
            
            start_menu = winshell.start_menu()
            start_shortcut_path = os.path.join(start_menu, "POS RestauranteFast.lnk")
            self.check_item("Acceso directo en menú inicio", os.path.exists(start_shortcut_path),
                           "Ejecutar create_shortcuts.py o install_windows11.ps1")
        except ImportError:
            self.check_item("Bibliotecas Windows", False,
                           "Instalar winshell y pywin32 para accesos directos")
    
    def test_application_launch(self):
        """Probar lanzamiento de la aplicación"""
        print("\n🎯 PRUEBA DE LANZAMIENTO:")
        print("─" * 40)
        
        try:
            # Intentar importar los módulos principales sin ejecutar GUI
            sys.path.insert(0, str(self.project_path))
            
            # Test de importaciones básicas
            try:
                import config
                self.check_item("Configuración importable", True)
            except Exception as e:
                self.check_item("Configuración importable", False, str(e))
            
            try:
                from models.user import User
                self.check_item("Modelos importables", True)
            except Exception as e:
                self.check_item("Modelos importables", False, str(e))
            
            try:
                from utils.database import DatabaseManager
                self.check_item("Utilidades importables", True)
            except Exception as e:
                self.check_item("Utilidades importables", False, str(e))
                
        except Exception as e:
            self.check_item("Módulos principales", False, str(e))
    
    def show_summary(self):
        """Mostrar resumen de la verificación"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE VERIFICACIÓN")
        print("=" * 60)
        
        success_rate = (self.success_count / self.total_checks) * 100 if self.total_checks > 0 else 0
        
        print(f"✅ Verificaciones exitosas: {self.success_count}/{self.total_checks} ({success_rate:.1f}%)")
        print(f"❌ Errores encontrados: {len(self.errors)}")
        print(f"⚠️  Advertencias: {len(self.warnings)}")
        
        if self.errors:
            print("\n❌ ERRORES A CORREGIR:")
            print("─" * 40)
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️  ADVERTENCIAS:")
            print("─" * 40)
            for warning in self.warnings:
                print(f"  {warning}")
        
        # Determinar estado general
        if len(self.errors) == 0:
            if len(self.warnings) == 0:
                print("\n🎉 ¡SISTEMA LISTO PARA TESTING!")
                print("   Todo está configurado correctamente.")
            else:
                print("\n✅ SISTEMA FUNCIONAL CON ADVERTENCIAS")
                print("   La aplicación debería funcionar, pero revisa las advertencias.")
        else:
            print("\n🔧 SISTEMA REQUIERE CORRECCIONES")
            print("   Corrige los errores antes de proceder con el testing.")
        
        print("\n🚀 PRÓXIMOS PASOS:")
        print("─" * 40)
        if len(self.errors) == 0:
            print("1. 🎯 Ejecutar aplicación: Doble click en POS_Windows11.bat")
            print("2. 🔐 Login inicial: admin / admin123")
            print("3. 🛍️  Configurar productos y categorías")
            print("4. 💰 Procesar ventas de prueba")
            print("5. 📊 Generar reportes")
        else:
            print("1. 🔧 Corregir errores listados arriba")
            print("2. 🔄 Ejecutar este script nuevamente")
            print("3. 📥 Si persisten errores, revisar instalación de Python")
        
        print("\n📖 DOCUMENTACIÓN:")
        print("─" * 40)
        print("• README_WINDOWS11.md - Guía completa de instalación")
        print("• README_SHORTCUTS.md - Instrucciones de uso")
        
        return len(self.errors) == 0
    
    def run_validation(self):
        """Ejecutar validación completa"""
        print("🔍 VALIDADOR DE INSTALACIÓN - POS RestauranteFast")
        print("=" * 60)
        print(f"🖥️  Sistema: {platform.system()} {platform.release()}")
        print(f"📁 Directorio: {self.project_path}")
        
        # Ejecutar todas las verificaciones
        self.check_python_installation()
        self.check_dependencies()
        self.check_project_files()
        self.check_database()
        self.check_launcher_files()
        self.check_shortcuts()
        self.test_application_launch()
        
        # Mostrar resumen
        return self.show_summary()

def main():
    """Función principal"""
    validator = Windows11Validator()
    success = validator.run_validation()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 ¡Validación completada exitosamente!")
    else:
        print("🔧 Validación completada con errores. Revisar arriba.")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
