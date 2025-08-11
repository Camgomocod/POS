#!/usr/bin/env python3
"""
Ejecutor seguro de la aplicación POS con debug completo
"""

import sys
import os
import traceback
import signal

# Configurar entorno para Windows
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

def signal_handler(signum, frame):
    """Manejador de señales"""
    print(f"\n🚨 Señal {signum} recibida")
    sys.exit(0)

# Configurar señales
signal.signal(signal.SIGINT, signal_handler)

print("🚀 EJECUTOR SEGURO - SISTEMA POS")
print("=" * 35)

try:
    # Agregar directorio del proyecto
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    print(f"📁 Directorio: {project_dir}")

    # 1. Verificar PyQt5
    print("\n1. Verificando PyQt5...")
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt, QCoreApplication
    print("✅ PyQt5 importado")

    # 2. Configurar aplicación Qt
    print("\n2. Configurando aplicación Qt...")
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("POS RestauranteFast")
    app.setStyle('Fusion')
    print("✅ QApplication configurada")

    # 3. Inicializar base de datos
    print("\n3. Inicializando base de datos...")
    from utils.database import init_database
    init_database()
    print("✅ Base de datos lista")

    # 4. Crear controlador
    print("\n4. Creando AppController...")
    from controllers.app_controller import AppController
    app_controller = AppController()
    app.app_controller = app_controller
    print("✅ AppController creado")

    # 5. Mostrar mensaje de confirmación
    print("\n5. Mostrando ventana de confirmación...")
    msg = QMessageBox()
    msg.setWindowTitle("POS - Test")
    msg.setText("¿Ves esta ventana?\n\nSi SÍ: PyQt5 funciona correctamente\nSi NO: Hay problema con PyQt5")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.Yes)
    
    result = msg.exec_()
    
    if result == QMessageBox.Yes:
        print("✅ Usuario confirmó que ve la ventana")
        
        # 6. Iniciar aplicación real
        print("\n6. Iniciando aplicación POS...")
        print("   👀 BUSCA LA VENTANA DE LOGIN - puede aparecer detrás de otras ventanas")
        
        app_controller.start_application()
        
        print("✅ Aplicación iniciada - ejecutando bucle principal...")
        exit_code = app.exec_()
        print(f"✅ Aplicación cerrada con código: {exit_code}")
        
    else:
        print("❌ Usuario no pudo ver la ventana - problema con PyQt5")
        print("\n💡 Soluciones:")
        print("   1. Instalar Visual C++ Redistributable 2015-2019")
        print("   2. Desactivar antivirus temporalmente")
        print("   3. Ejecutar como administrador")
        
except Exception as e:
    print(f"\n❌ ERROR CRÍTICO: {e}")
    print("\n📋 TRACEBACK COMPLETO:")
    traceback.print_exc()
    
    # Intentar mostrar error en ventana si es posible
    try:
        from PyQt5.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication([])
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error POS")
        msg.setText(f"Error crítico: {str(e)}")
        msg.setDetailedText(traceback.format_exc())
        msg.exec_()
    except:
        pass

finally:
    print("\n" + "="*50)
    print("🔄 Limpiando y cerrando...")
    try:
        app = QApplication.instance()
        if app:
            app.quit()
    except:
        pass
    print("✅ Proceso completado")

input("\nPresiona Enter para salir...")
