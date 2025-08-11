#!/usr/bin/env python3
"""
Test directo de la aplicación POS para identificar por qué no abre la interfaz
"""

import sys
import os
import traceback

# Configurar entorno
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

print("🔍 TEST DIRECTO DE APLICACIÓN POS")
print("=" * 35)

# 1. Test básico de PyQt5
print("\n1. Probando PyQt5 básico...")
try:
    from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
    from PyQt5.QtCore import Qt
    
    print("✅ PyQt5 importado correctamente")
    
    # Crear aplicación simple
    app = QApplication(sys.argv)
    print("✅ QApplication creada")
    
    # Crear ventana simple
    window = QMainWindow()
    window.setWindowTitle("Test POS - ¿Funciona?")
    window.setGeometry(100, 100, 300, 200)
    
    label = QLabel("SI VES ESTA VENTANA, PyQt5 FUNCIONA!")
    label.setAlignment(Qt.AlignCenter)
    window.setCentralWidget(label)
    
    print("✅ Ventana de test creada")
    
    # Mostrar ventana
    window.show()
    print("✅ Ventana mostrada - DEBERÍAS VER UNA VENTANA AHORA")
    print("   Si no ves una ventana, hay un problema con PyQt5 o el sistema")
    
    # Mantener ventana 3 segundos
    from PyQt5.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(3000)  # 3 segundos
    
    app.exec_()
    print("✅ Test de PyQt5 completado")
    
except Exception as e:
    print(f"❌ Error en test de PyQt5: {e}")
    traceback.print_exc()
    input("Presiona Enter para continuar...")

# 2. Test de importaciones del proyecto
print("\n2. Probando importaciones del proyecto...")
try:
    # Agregar directorio del proyecto al path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    from utils.database import init_database
    print("✅ utils.database importado")
    
    from controllers.app_controller import AppController
    print("✅ controllers.app_controller importado")
    
    from views.login_window import LoginWindow
    print("✅ views.login_window importado")
    
except Exception as e:
    print(f"❌ Error en importaciones: {e}")
    traceback.print_exc()

# 3. Test de base de datos
print("\n3. Probando base de datos...")
try:
    init_database()
    print("✅ Base de datos inicializada")
except Exception as e:
    print(f"❌ Error en base de datos: {e}")
    traceback.print_exc()

# 4. Test de creación de controlador
print("\n4. Probando creación de AppController...")
try:
    app = QApplication.instance() or QApplication(sys.argv)
    
    app_controller = AppController()
    print("✅ AppController creado")
    
    # NO llamar start_application aún, solo verificar que se puede crear
    
except Exception as e:
    print(f"❌ Error creando AppController: {e}")
    traceback.print_exc()

# 5. Test de ventana de login
print("\n5. Probando creación de LoginWindow...")
try:
    login_window = LoginWindow()
    print("✅ LoginWindow creada")
    
    # Mostrar por 2 segundos
    login_window.show()
    print("✅ LoginWindow mostrada - DEBERÍAS VER LA VENTANA DE LOGIN")
    
    from PyQt5.QtCore import QTimer
    timer = QTimer()
    timer.timeout.connect(login_window.close)
    timer.start(2000)  # 2 segundos
    
    app = QApplication.instance()
    app.processEvents()
    
    timer.timeout.connect(app.quit)
    app.exec_()
    
    print("✅ Test de LoginWindow completado")
    
except Exception as e:
    print(f"❌ Error en LoginWindow: {e}")
    traceback.print_exc()

print("\n" + "="*50)
print("📋 RESUMEN DEL TEST:")
print("   Si viste las ventanas aparecer, el problema está en otro lado")
print("   Si NO viste ventanas, hay un problema con PyQt5 o el sistema")
print("="*50)

input("\nPresiona Enter para salir...")
