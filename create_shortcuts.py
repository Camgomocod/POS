#!/usr/bin/env python3
"""
Script para crear acceso directo al Sistema POS
Facilita el testing y uso diario sin necesidad de terminal
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class ShortcutCreator:
    """Creador de accesos directos multiplataforma"""
    
    def __init__(self):
        self.project_path = Path(__file__).parent.absolute()
        self.main_script = self.project_path / "main.py"
        self.icon_path = self.project_path / "assets" / "pos_icon.ico"
        self.system = platform.system()
        
    def detect_python_executable(self):
        """Detectar el ejecutable de Python correcto"""
        if self.system == "Windows":
            possible_pythons = [
                "py",
                "python",
                "python3",
                r"C:\Python312\python.exe",
                r"C:\Python311\python.exe",
                r"C:\Python310\python.exe",
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe",
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe",
                f"{os.path.expanduser('~')}/miniconda3/envs/POS/python.exe",
                f"{os.path.expanduser('~')}/anaconda3/envs/POS/python.exe",
            ]
        else:
            possible_pythons = [
                "python",
                "python3", 
                "py",
                f"{os.path.expanduser('~')}/miniconda3/envs/POS/bin/python",
                f"{os.path.expanduser('~')}/anaconda3/envs/POS/bin/python",
            ]
        
        for python_cmd in possible_pythons:
            try:
                result = subprocess.run([python_cmd, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Python encontrado: {python_cmd}")
                    return python_cmd
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        print("❌ No se pudo detectar Python automáticamente")
        return "python"
    
    def create_icon(self):
        """Crear un icono básico si no existe"""
        assets_dir = self.project_path / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        if not self.icon_path.exists():
            print("📎 Creando icono básico...")
            # Crear un archivo .ico básico (en sistemas reales usarías una imagen)
            try:
                # Crear un archivo placeholder
                with open(self.icon_path, 'w') as f:
                    f.write("# POS Icon Placeholder")
                print(f"✅ Icono creado en: {self.icon_path}")
            except Exception as e:
                print(f"⚠️  No se pudo crear icono: {e}")
    
    def create_windows_shortcut(self):
        """Crear acceso directo para Windows"""
        try:
            import winshell
            from win32com.client import Dispatch
        except ImportError:
            print("❌ Bibliotecas de Windows no disponibles")
            print("💡 Instalar con: pip install winshell pywin32")
            print("📝 Creando archivo .bat alternativo...")
            return self.create_batch_file_windows()
        
        try:
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "POS RestauranteFast.lnk")
            
            # Usar POS_Windows11.bat como target para mejor compatibilidad
            batch_file = self.project_path / "POS_Windows11.bat"
            if not batch_file.exists():
                self.create_batch_file_windows()
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = str(batch_file)
            shortcut.WorkingDirectory = str(self.project_path)
            shortcut.IconLocation = str(self.icon_path)
            shortcut.Description = "Sistema POS para Restaurantes - Windows 11"
            shortcut.save()
            
            # Crear también en Start Menu
            start_menu = winshell.start_menu()
            start_shortcut_path = os.path.join(start_menu, "POS RestauranteFast.lnk")
            start_shortcut = shell.CreateShortCut(start_shortcut_path)
            start_shortcut.Targetpath = str(batch_file)
            start_shortcut.WorkingDirectory = str(self.project_path)
            start_shortcut.IconLocation = str(self.icon_path)
            start_shortcut.Description = "Sistema POS para Restaurantes - Windows 11"
            start_shortcut.save()
            
            print(f"✅ Acceso directo creado en escritorio: {shortcut_path}")
            print(f"✅ Acceso directo creado en menú inicio: {start_shortcut_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando acceso directo Windows: {e}")
            print("📝 Creando archivo .bat alternativo...")
            return self.create_batch_file_windows()
    
    def create_linux_shortcut(self):
        """Crear acceso directo para Linux"""
        try:
            desktop_dir = Path.home() / "Desktop"
            applications_dir = Path.home() / ".local" / "share" / "applications"
            
            # Crear directorios si no existen
            applications_dir.mkdir(parents=True, exist_ok=True)
            
            python_exe = self.detect_python_executable()
            
            # Contenido del archivo .desktop
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=POS RestauranteFast
Comment=Sistema POS para Restaurantes
Exec={python_exe} "{self.main_script}"
Icon={self.icon_path}
Path={self.project_path}
Terminal=false
StartupNotify=true
Categories=Office;Finance;
Keywords=POS;Restaurant;Sales;
"""
            
            # Crear archivo en applications
            app_file = applications_dir / "pos-restaurant.desktop"
            with open(app_file, 'w') as f:
                f.write(desktop_content)
            
            # Hacer ejecutable
            app_file.chmod(0o755)
            
            # Crear también en Desktop si existe
            if desktop_dir.exists():
                desktop_file = desktop_dir / "POS RestauranteFast.desktop"
                with open(desktop_file, 'w') as f:
                    f.write(desktop_content)
                desktop_file.chmod(0o755)
                print(f"✅ Acceso directo creado en: {desktop_file}")
            
            print(f"✅ Aplicación agregada al menú: {app_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando acceso directo Linux: {e}")
            return False
    
    def create_macos_shortcut(self):
        """Crear acceso directo para macOS"""
        try:
            applications_dir = Path.home() / "Applications"
            app_dir = applications_dir / "POS RestauranteFast.app"
            contents_dir = app_dir / "Contents"
            macos_dir = contents_dir / "MacOS"
            resources_dir = contents_dir / "Resources"
            
            # Crear estructura de directorios
            macos_dir.mkdir(parents=True, exist_ok=True)
            resources_dir.mkdir(parents=True, exist_ok=True)
            
            python_exe = self.detect_python_executable()
            
            # Crear script ejecutable
            executable_script = macos_dir / "POS RestauranteFast"
            script_content = f"""#!/bin/bash
cd "{self.project_path}"
{python_exe} "{self.main_script}"
"""
            
            with open(executable_script, 'w') as f:
                f.write(script_content)
            executable_script.chmod(0o755)
            
            # Crear Info.plist
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>POS RestauranteFast</string>
    <key>CFBundleIdentifier</key>
    <string>com.restaurant.pos</string>
    <key>CFBundleName</key>
    <string>POS RestauranteFast</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
"""
            
            plist_file = contents_dir / "Info.plist"
            with open(plist_file, 'w') as f:
                f.write(plist_content)
            
            print(f"✅ Aplicación creada en: {app_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando aplicación macOS: {e}")
            return False
    
    def create_batch_file_windows(self):
        """Crear archivo .bat como alternativa en Windows"""
        try:
            # Crear el archivo batch avanzado que ya creamos
            batch_content = '''@echo off
rem POS RestauranteFast - Launcher para Windows 11
title POS RestauranteFast
color 0A

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║                    POS RestauranteFast                        ║
echo  ║              Sistema de Punto de Venta                       ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.
echo  🚀 Iniciando aplicacion...

cd /d "%~dp0"

if not exist "main.py" (
    echo  ❌ Error: No se encontro main.py en este directorio
    pause
    exit /b 1
)

rem Intentar py primero (recomendado para Windows)
py --version >nul 2>&1
if %errorlevel%==0 (
    echo  ✅ Ejecutando con py...
    py main.py
    goto :end
)

rem Intentar python
python --version >nul 2>&1
if %errorlevel%==0 (
    echo  ✅ Ejecutando con python...
    python main.py
    goto :end
)

rem Intentar python3
python3 --version >nul 2>&1
if %errorlevel%==0 (
    echo  ✅ Ejecutando con python3...
    python3 main.py
    goto :end
)

echo  ❌ Error: No se pudo encontrar Python
echo  📥 Instala Python desde: https://python.org
echo  ⚠️  Marca "Add to PATH" durante la instalacion

:end
if %errorlevel% neq 0 (
    echo.
    echo  📋 CREDENCIALES: admin/admin123 o cajero/cajero123
    pause
)
'''
            
            batch_file = self.project_path / "POS_Windows11.bat"
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(batch_content)
            
            print(f"✅ Archivo batch Windows 11 creado: {batch_file}")
            print("💡 Doble click en POS_Windows11.bat para ejecutar")
            
            # Crear también el batch simple original como backup
            simple_batch = self.project_path / "POS_RestauranteFast.bat"
            python_exe = self.detect_python_executable()
            simple_content = f'''@echo off
title POS RestauranteFast
cd /d "%~dp0"
{python_exe} "{self.main_script}"
if %errorlevel% neq 0 pause
'''
            with open(simple_batch, 'w', encoding='utf-8') as f:
                f.write(simple_content)
            
            print(f"✅ Archivo batch simple creado: {simple_batch}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando archivo batch: {e}")
            return False
    
    def create_shell_script_unix(self):
        """Crear script shell para Linux/macOS"""
        try:
            python_exe = self.detect_python_executable()
            script_content = f"""#!/bin/bash
# Script de lanzamiento POS RestauranteFast
cd "{self.project_path}"
{python_exe} "{self.main_script}"
"""
            
            script_file = self.project_path / "run_pos.sh"
            with open(script_file, 'w') as f:
                f.write(script_content)
            script_file.chmod(0o755)
            
            print(f"✅ Script shell creado: {script_file}")
            print("💡 Ejecutar con: ./run_pos.sh")
            return True
            
        except Exception as e:
            print(f"❌ Error creando script shell: {e}")
            return False
    
    def create_shortcuts(self):
        """Crear accesos directos según el sistema operativo"""
        print("🚀 Creador de Accesos Directos - POS RestauranteFast")
        print("=" * 60)
        print(f"🖥️  Sistema operativo: {self.system}")
        print(f"📁 Directorio del proyecto: {self.project_path}")
        print(f"🐍 Script principal: {self.main_script}")
        print()
        
        # Verificar que el script principal existe
        if not self.main_script.exists():
            print(f"❌ No se encontró main.py en: {self.main_script}")
            return False
        
        # Crear icono básico
        self.create_icon()
        
        success = False
        
        if self.system == "Windows":
            print("🪟 Creando accesos directos para Windows 11...")
            # Crear primero el archivo batch optimizado
            self.create_batch_file_windows()
            
            # Intentar crear acceso directo nativo
            if not self.create_windows_shortcut():
                print("📝 Usando archivo .bat como método principal")
                success = True  # El batch file ya fue creado
            else:
                success = True
                
        elif self.system == "Linux":
            print("🐧 Creando accesos directos para Linux...")
            success = self.create_linux_shortcut()
            # Crear también script shell como backup
            self.create_shell_script_unix()
            
        elif self.system == "Darwin":  # macOS
            print("🍎 Creando aplicación para macOS...")
            success = self.create_macos_shortcut()
            # Crear también script shell como backup
            self.create_shell_script_unix()
            
        else:
            print(f"⚠️  Sistema {self.system} no reconocido, creando script genérico...")
            success = self.create_shell_script_unix()
        
        if success:
            print("\n✅ ¡Accesos directos creados exitosamente!")
            print("\n📋 INSTRUCCIONES DE USO:")
            print("─" * 30)
            
            if self.system == "Windows":
                print("🪟 Windows 11:")
                print("   • Busca 'POS RestauranteFast' en el escritorio")
                print("   • O busca en el menú inicio")
                print("   • O ejecuta 'POS_Windows11.bat' en esta carpeta")
                print("   • Para instalar completamente: .\\install_windows11.ps1 -All")
                
            elif self.system == "Linux":
                print("🐧 Linux:")
                print("   • Busca 'POS RestauranteFast' en el menú de aplicaciones")
                print("   • O ejecuta './run_pos.sh' en terminal desde esta carpeta")
                
            elif self.system == "Darwin":
                print("🍎 macOS:")
                print("   • Busca 'POS RestauranteFast' en la carpeta Aplicaciones")
                print("   • O ejecuta './run_pos.sh' en terminal desde esta carpeta")
            
            print("\n🔐 CREDENCIALES DE ACCESO:")
            print("   👑 Admin: admin / admin123")
            print("   💰 Cajero: cajero / cajero123")
            
        else:
            print("\n❌ No se pudieron crear todos los accesos directos")
            print("💡 Puedes ejecutar manualmente con: python main.py")
        
        return success

def main():
    """Función principal"""
    creator = ShortcutCreator()
    creator.create_shortcuts()

if __name__ == "__main__":
    main()
