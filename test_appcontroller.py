#!/usr/bin/env python3
"""
Test específico para identificar dónde se cuelga el AppController
"""

import sys
import os
import traceback

# Configurar entorno
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

# Agregar directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

print("🔍 TEST ESPECÍFICO DE AppController")
print("=" * 40)

try:
    # 1. PyQt5 básico
    print("1. Importando PyQt5...")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QObject, pyqtSignal
    app = QApplication(sys.argv)
    print("✅ PyQt5 y QApplication OK")

    # 2. Importar modelos
    print("\n2. Importando modelos...")
    from models.user import UserRole
    print("✅ models.user OK")

    # 3. Importar vistas UNA POR UNA
    print("\n3. Importando vistas...")
    
    print("   3a. Importando LoginWindow...")
    try:
        from views.login_window import LoginWindow
        print("   ✅ LoginWindow importado")
    except Exception as e:
        print(f"   ❌ Error en LoginWindow: {e}")
        traceback.print_exc()
        input("Presiona Enter para salir...")
        sys.exit(1)

    print("   3b. Probando crear LoginWindow...")
    try:
        # Solo crear, no mostrar aún
        login_test = LoginWindow()
        print("   ✅ LoginWindow creado exitosamente")
        login_test.deleteLater()
    except Exception as e:
        print(f"   ❌ Error creando LoginWindow: {e}")
        traceback.print_exc()
        input("Presiona Enter para salir...")
        sys.exit(1)

    print("   3c. Importando POSWindow...")
    try:
        from views.pos_window import POSWindow
        print("   ✅ POSWindow importado")
    except Exception as e:
        print(f"   ❌ Error en POSWindow: {e}")
        traceback.print_exc()
        # Continuar sin POSWindow por ahora

    print("   3d. Importando AdminWindow...")
    try:
        from views.admin_window import AdminWindow
        print("   ✅ AdminWindow importado")
    except Exception as e:
        print(f"   ❌ Error en AdminWindow: {e}")
        traceback.print_exc()
        # Continuar sin AdminWindow por ahora

    # 4. Crear AppController paso a paso
    print("\n4. Creando AppController paso a paso...")
    
    print("   4a. Definiendo clase AppController...")
    from controllers.app_controller import AppController
    print("   ✅ Clase AppController importada")
    
    print("   4b. Creando instancia de AppController...")
    print("       (Si se cuelga aquí, hay problema en __init__)")
    
    app_controller = AppController()
    print("   ✅ AppController creado exitosamente!")
    
    # 5. Test de métodos básicos
    print("\n5. Probando métodos de AppController...")
    
    print("   5a. Probando close_all_windows...")
    app_controller.close_all_windows()
    print("   ✅ close_all_windows OK")
    
    print("   5b. Probando show_login (SIN ejecutar app.exec)...")
    try:
        app_controller.show_login()
        print("   ✅ show_login ejecutado")
        
        # Procesar eventos para que se muestre la ventana
        app.processEvents()
        print("   ✅ Eventos procesados - DEBERÍAS VER LA VENTANA DE LOGIN")
        
        # Cerrar inmediatamente
        app_controller.close_all_windows()
        print("   ✅ Ventana cerrada")
        
    except Exception as e:
        print(f"   ❌ Error en show_login: {e}")
        traceback.print_exc()

    print("\n🎉 ¡TODOS LOS TESTS PASARON!")
    print("   El AppController funciona correctamente")
    print("   El problema puede estar en el bucle de eventos (app.exec)")

except Exception as e:
    print(f"\n❌ ERROR EN TEST: {e}")
    traceback.print_exc()

finally:
    print("\n" + "="*50)
    print("📋 CONCLUSIONES:")
    print("   Si todos los tests pasaron: el problema está en app.exec()")
    print("   Si algún test falló: ese es el problema específico")
    print("="*50)

input("\nPresiona Enter para salir...")
