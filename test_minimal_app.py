#!/usr/bin/env python3
"""
Test usando AppController minimal (sin AdminWindow)
"""

import sys
import os

# Configurar entorno
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

# Agregar directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

print("🧪 TEST CON AppController MINIMAL")
print("=" * 35)

try:
    print("1. Configurando PyQt5...")
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt, QCoreApplication
    
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("POS Test Minimal")
    print("✅ PyQt5 configurado")

    print("\n2. Inicializando base de datos...")
    from utils.database import init_database
    init_database()
    print("✅ Base de datos lista")

    print("\n3. Importando AppController MINIMAL...")
    from app_controller_minimal import AppControllerMinimal
    print("✅ AppController minimal importado")

    print("\n4. Creando AppController minimal...")
    app_controller = AppControllerMinimal()
    app.app_controller = app_controller
    print("✅ AppController minimal creado")

    print("\n5. Iniciando aplicación...")
    app_controller.start_application()
    print("✅ Aplicación iniciada")

    print("\n6. Procesando eventos...")
    app.processEvents()
    print("✅ Eventos procesados")

    # Mensaje de confirmación
    msg = QMessageBox()
    msg.setWindowTitle("Test Minimal")
    msg.setText("AppController Minimal Test\n\n¿Ves la ventana de login?\n\nEsto confirma que el problema está en AdminWindow")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg.exec_()

    if result == QMessageBox.Yes:
        print("✅ ¡CONFIRMADO! El problema está en AdminWindow")
        print("   La aplicación funciona sin AdminWindow")
        
        # Preguntar si quiere continuar con la app
        msg2 = QMessageBox()
        msg2.setWindowTitle("Continuar")
        msg2.setText("¿Quieres usar la aplicación sin funciones de admin por ahora?")
        msg2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result2 = msg2.exec_()
        
        if result2 == QMessageBox.Yes:
            print("🚀 Ejecutando aplicación en modo limitado...")
            return app.exec_()
        
    else:
        print("❌ Aún hay problemas - puede ser LoginWindow o POSWindow")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n✅ Test completado")

input("\nPresiona Enter para salir...")
