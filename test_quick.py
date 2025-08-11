#!/usr/bin/env python3
"""
Test rápido después de corregir matplotlib
"""

import os
import sys

# Configurar entorno
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
os.environ['DISABLE_MATPLOTLIB'] = '1'

# Agregar directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

print("🧪 TEST RÁPIDO POST-CORRECCIÓN")
print("=" * 30)

try:
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    print("1. ✅ PyQt5 OK")
    
    from utils.database import init_database
    init_database()
    print("2. ✅ Base de datos OK")
    
    from controllers.app_controller import AppController
    print("3. ✅ AppController importado")
    
    app_controller = AppController()
    print("4. ✅ AppController creado")
    
    app_controller.start_application()
    print("5. ✅ Aplicación iniciada")
    
    print("\n🎉 ¡FUNCIONANDO! La aplicación debería estar abierta")
    print("   Si aparece el login, el problema está resuelto")
    
    # Ejecutar por un tiempo limitado para testing
    from PyQt5.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(30000)  # 30 segundos máximo
    
    exit_code = app.exec_()
    print(f"✅ Aplicación cerrada (código: {exit_code})")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("✅ Test completado")

input("Presiona Enter para salir...")
