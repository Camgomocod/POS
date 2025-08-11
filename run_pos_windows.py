#!/usr/bin/env python3
"""
Script para ejecutar POS con PyQtGraph
Ahora usa PyQtGraph en lugar de matplotlib para gráficos
"""

import sys
import os

# Configurar entorno
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

# Agregar directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

print("🚀 POS SIN MATPLOTLIB (SOLUCIÓN TEMPORAL)")
print("=" * 45)

try:
    print("1. Configurando PyQt5...")
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt, QCoreApplication
    
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("POS RestauranteFast")
    app.setStyle('Fusion')
    print("✅ PyQt5 configurado")

    print("\n2. Inicializando base de datos...")
    from utils.database import init_database
    init_database()
    print("✅ Base de datos lista")

    print("\n3. Importando AppController...")
    from controllers.app_controller import AppController
    print("✅ AppController importado")

    print("\n4. Creando AppController...")
    app_controller = AppController()
    app.app_controller = app_controller
    print("✅ AppController creado")

    print("\n5. Iniciando aplicación...")
    app_controller.start_application()
    print("✅ Aplicación iniciada")

    print("\n🎉 ¡POS FUNCIONANDO!")
    print("   Las gráficas de reportes estarán deshabilitadas temporalmente")
    print("   Pero todas las demás funciones funcionan normalmente")

    # Ejecutar aplicación
    exit_code = app.exec_()
    print(f"✅ Aplicación cerrada correctamente (código: {exit_code})")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Mostrar error al usuario
    try:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error POS")
        msg.setText(f"Error al iniciar POS: {str(e)}")
        msg.exec_()
    except:
        pass

finally:
    print("\n✅ Proceso completado")

input("\nPresiona Enter para salir...")
