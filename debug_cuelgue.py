#!/usr/bin/env python3
"""
Versión debug del ejecutor que identifica exactamente dónde se cuelga
"""

import sys
import os
import traceback
import signal
import threading
import time

# Configurar entorno
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

# Agregar directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

def timeout_handler():
    """Handler para timeout - si se cuelga más de 10 segundos"""
    time.sleep(10)
    print("\n⏰ TIMEOUT: El proceso se colgó por más de 10 segundos")
    print("   Esto indica un problema específico en el código")
    os._exit(1)

# Iniciar thread de timeout
timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
timeout_thread.start()

print("🐛 EJECUTOR DEBUG - IDENTIFICAR CUELGUE")
print("=" * 42)

try:
    print("Paso 1: Configurando PyQt5...")
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt, QCoreApplication
    print("✅ PyQt5 importado")

    print("\nPaso 2: Creando QApplication...")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("POS Debug")
    print("✅ QApplication creada")

    print("\nPaso 3: Importando utils.database...")
    from utils.database import init_database
    print("✅ utils.database importado")

    print("\nPaso 4: Inicializando base de datos...")
    init_database()
    print("✅ Base de datos inicializada")

    print("\nPaso 5: Importando AppController...")
    from controllers.app_controller import AppController
    print("✅ AppController importado")

    print("\nPaso 6: CREANDO AppController (aquí se puede colgar)...")
    print("         Si no aparece el mensaje de éxito, se colgó en __init__")
    
    app_controller = AppController()
    print("✅ AppController CREADO EXITOSAMENTE!")

    print("\nPaso 7: Asignando app_controller a app...")
    app.app_controller = app_controller
    print("✅ Asignación completada")

    print("\nPaso 8: Probando start_application...")
    print("         Si no aparece mensaje de éxito, se cuelga en start_application")
    
    # Ejecutar start_application sin el bucle principal
    app_controller.start_application()
    print("✅ start_application COMPLETADO!")

    print("\nPaso 9: Procesando eventos...")
    app.processEvents()
    print("✅ Eventos procesados")

    print("\n🎉 TODOS LOS PASOS COMPLETADOS SIN COLGARSE!")
    print("   La aplicación debería estar funcionando")
    print("   ¿Ves la ventana de login?")

    # Mostrar mensaje de confirmación
    msg = QMessageBox()
    msg.setWindowTitle("Debug - ¿Funciona?")
    msg.setText("¿Ves la ventana de login del POS?\n\nSí = Todo OK\nNo = Ventana invisible")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg.exec_()

    if result == QMessageBox.Yes:
        print("✅ Usuario confirmó que ve la ventana de login")
        print("🎉 ¡PROBLEMA RESUELTO! La aplicación funciona correctamente")
    else:
        print("❌ Usuario no ve la ventana de login")
        print("💡 La ventana se crea pero no es visible - problema de visualización")

except Exception as e:
    print(f"\n❌ ERROR EN PASO ESPECÍFICO: {e}")
    print("\n📋 TRACEBACK:")
    traceback.print_exc()
    
    print(f"\n💡 El error ocurrió en uno de los pasos anteriores")
    print("   Esto nos ayuda a identificar exactamente dónde está el problema")

finally:
    print("\n" + "="*50)
    print("🔚 Debug completado")
    try:
        app = QApplication.instance()
        if app:
            app.quit()
    except:
        pass

input("\nPresiona Enter para salir...")
