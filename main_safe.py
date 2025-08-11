#!/usr/bin/env python3
"""
Versión simplificada del main.py sin matplotlib para evitar Access Violation
"""

import sys
import os

# Configurar PyQt5 para Windows antes de cualquier importación
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'
os.environ['QT_SCALE_FACTOR'] = '1'
os.environ['QT_DEVICE_PIXEL_RATIO'] = '1'
os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'

try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt
    import traceback
    
    print("🚀 Iniciando Sistema POS - Modo Seguro")
    print("💡 Gráficos avanzados temporalmente deshabilitados")
    print()
    
    # Crear aplicación PyQt5 con configuración segura
    app = QApplication(sys.argv)
    
    # Configurar aplicación para evitar problemas gráficos
    app.setAttribute(Qt.AA_EnableHighDpiScaling, False)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, False)
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)
    
    try:
        # Importar el controlador principal
        from controllers.app_controller import AppController
        
        # Crear y ejecutar controlador
        controller = AppController()
        controller.start()
        
        # Ejecutar aplicación
        sys.exit(app.exec_())
        
    except ImportError as e:
        error_msg = f"Error de importación: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Mostrar error en ventana
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error de Importación")
        msg.setText(f"Error al importar módulos:\n\n{error_msg}\n\nVerifica que todas las dependencias estén instaladas.")
        msg.setDetailedText(traceback.format_exc())
        msg.exec_()
        
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Mostrar error en ventana
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error del Sistema")
        msg.setText(f"Error inesperado en el sistema:\n\n{error_msg}")
        msg.setDetailedText(traceback.format_exc())
        msg.exec_()
        
        sys.exit(1)

except ImportError:
    print("❌ Error crítico: PyQt5 no está instalado o configurado correctamente")
    print()
    print("🔧 Soluciones:")
    print("   1. pip install PyQt5==5.15.9")
    print("   2. Ejecutar: fix_access_violation.bat")
    print("   3. Verificar entorno virtual")
    print()
    input("Presiona Enter para salir...")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error crítico del sistema: {e}")
    print()
    print("🔧 Ejecutar: fix_access_violation.bat")
    print()
    input("Presiona Enter para salir...")
    sys.exit(1)
