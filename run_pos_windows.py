#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher para Windows - POS RestauranteFast
Configura la codificación correcta y ejecuta la aplicación
"""

import sys
import os
import subprocess
import platform

# Configurar encoding para Windows
if platform.system() == "Windows":
    import locale
    # Configurar UTF-8 para Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Intentar configurar la consola para UTF-8
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except:
        pass

def clear_screen():
    """Limpiar pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Mostrar banner de bienvenida"""
    print("\n" + "="*65)
    print("|                    POS RestauranteFast                    |")
    print("|              Sistema de Punto de Venta                   |")
    print("="*65)
    print("\nIniciando aplicacion...\n")

def show_error_banner():
    """Mostrar banner de error"""
    print("\n" + "="*65)
    print("|                      ERROR                                |")
    print("|         No se pudo iniciar la aplicacion                 |")
    print("="*65)

def show_credentials():
    """Mostrar credenciales de acceso"""
    print("\nCREDENCIALES DE ACCESO:")
    print("-" * 40)
    print("Admin:  admin / admin123")
    print("Cajero: cajero / cajero123")
    print("-" * 40)

def main():
    """Función principal"""
    clear_screen()
    show_banner()
    
    # Verificar que main.py existe
    if not os.path.exists("main.py"):
        show_error_banner()
        print("Error: No se encontro main.py en este directorio")
        print(f"Directorio actual: {os.getcwd()}")
        print("\nAsegurate de ejecutar este archivo desde la carpeta del proyecto POS")
        show_credentials()
        input("\nPresiona Enter para cerrar...")
        return 1
    
    try:
        # Cambiar al directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        print("Detectando Python...")
        
        # Intentar ejecutar con el Python actual
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=False, 
                              text=True)
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n\nInterrupcion por teclado detectada")
        return 0
        
    except FileNotFoundError:
        show_error_banner()
        print("Error: No se pudo encontrar Python")
        print("\nSOLUCIONES POSIBLES:")
        print("1. Instalar Python desde: https://python.org")
        print("2. Verificar que Python este en PATH del sistema")
        print("3. Reinstalar Python marcando 'Add to PATH'")
        show_credentials()
        input("\nPresiona Enter para cerrar...")
        return 1
        
    except Exception as e:
        show_error_banner()
        print(f"Error inesperado: {e}")
        show_credentials()
        input("\nPresiona Enter para cerrar...")
        return 1

if __name__ == "__main__":
    exit_code = main()
    
    if exit_code == 0:
        print("\nAplicacion cerrada correctamente")
    else:
        show_credentials()
        input("\nPresiona Enter para cerrar...")
    
    sys.exit(exit_code)
