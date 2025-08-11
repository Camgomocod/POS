#!/usr/bin/env python3
"""
Versión SEGURA del Sistema POS - Sin componentes gráficos problemáticos
Para usar cuando hay problemas con Access Violation o matplotlib
"""

import sys
import os

def setup_safe_environment():
    """Configurar entorno seguro para PyQt5"""
    print("🔧 Configurando entorno seguro...")
    
    # Variables de entorno ANTES de importar PyQt5
    os.environ['QT_QPA_PLATFORM'] = 'windows'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'
    os.environ['QT_SCALE_FACTOR'] = '1'
    os.environ['QT_DEVICE_PIXEL_RATIO'] = '1'
    os.environ['QT_SCREEN_SCALE_FACTORS'] = '1'
    os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
    os.environ['QT_USE_PHYSICAL_DPI'] = 'false'
    
    # Matplotlib backend seguro (sin tkinter)
    os.environ['MPLBACKEND'] = 'Agg'
    os.environ['MATPLOTLIB_BACKEND'] = 'Agg'
    
def main():
    print("🚀 Iniciando Sistema POS - Modo Seguro")
    print("💡 Gráficos avanzados temporalmente deshabilitados")
    
    try:
        # Configurar entorno ANTES de cualquier import PyQt5
        setup_safe_environment()
        
        # IMPORTANTE: Configurar atributos ANTES de cualquier import PyQt5
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        # Configurar atributos ANTES de crear QApplication
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False)
        QApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)
        
        # Crear aplicación DESPUÉS de configurar atributos
        app = QApplication(sys.argv)
        
        print("✅ PyQt5 configurado correctamente")
        
        # Importar controlador principal
        from controllers.app_controller import AppController
        
        print("✅ Controladores importados")
        
        # Inicializar aplicación
        controller = AppController()
        
        print("✅ Sistema inicializado en modo seguro")
        print("🎯 Funcionalidades disponibles:")
        print("   - ✅ Login de usuarios")
        print("   - ✅ POS (Punto de Venta)")
        print("   - ✅ Gestión de productos")
        print("   - ✅ Gestión de órdenes")
        print("   - ✅ Administración de usuarios")
        print("   - ⚠️  Reportes gráficos: DESHABILITADOS (modo seguro)")
        print("")
        print("💡 Para habilitar gráficos, ejecuta: fix_access_violation.bat")
        print("📱 Sistema listo para usar!")
        
        # Ejecutar aplicación
        controller.show_login()
        sys.exit(app.exec_())
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("")
        print("🔧 Posibles soluciones:")
        print("1. pip install -r requirements.txt")
        print("2. Ejecutar: fix_dependencies.bat")
        print("3. Verificar que estás en el directorio correcto")
        
        input("\nPresiona Enter para salir...")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("")
        print("🔧 Posibles soluciones:")
        print("1. Ejecutar: fix_access_violation.bat")
        print("2. Verificar permisos de Windows")
        print("3. Ejecutar como Administrador")
        
        input("\nPresiona Enter para salir...")
        return False

if __name__ == "__main__":
    # Configurar encoding para Windows
    try:
        import locale
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except:
        pass
    
    # Ejecutar aplicación
    success = main()
    if not success:
        sys.exit(1)
