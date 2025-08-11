#!/usr/bin/env python3
"""
Test mínimo de PyQt5 para Windows 11
Ejecutar este script para verificar que PyQt5 funciona básicamente
"""

import sys
import platform

def test_pyqt5_basic():
    """Test básico de PyQt5"""
    print("🧪 Test Mínimo de PyQt5 para Windows 11")
    print("=" * 45)
    
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print()
    
    # Test 1: Importar PyQt5
    print("1. Importando PyQt5...")
    try:
        from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
        from PyQt5.QtCore import Qt
        print("   ✅ PyQt5 importado correctamente")
    except ImportError as e:
        print(f"   ❌ Error al importar PyQt5: {e}")
        return False
    
    # Test 2: Crear aplicación
    print("2. Creando QApplication...")
    try:
        app = QApplication(sys.argv)
        print("   ✅ QApplication creada")
    except Exception as e:
        print(f"   ❌ Error al crear QApplication: {e}")
        return False
    
    # Test 3: Crear ventana simple
    print("3. Creando ventana de prueba...")
    try:
        window = QWidget()
        window.setWindowTitle("Test PyQt5 - POS Windows 11")
        window.setGeometry(300, 300, 400, 200)
        
        layout = QVBoxLayout()
        
        # Etiquetas de información
        label1 = QLabel("✅ PyQt5 funciona correctamente!")
        label1.setAlignment(Qt.AlignCenter)
        
        label2 = QLabel(f"Python: {platform.python_version()}")
        label2.setAlignment(Qt.AlignCenter)
        
        label3 = QLabel(f"Sistema: {platform.system()} {platform.release()}")
        label3.setAlignment(Qt.AlignCenter)
        
        # Botón de cerrar
        close_button = QPushButton("Cerrar Test")
        close_button.clicked.connect(window.close)
        
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(close_button)
        
        window.setLayout(layout)
        
        print("   ✅ Ventana creada correctamente")
        
        # Mostrar ventana
        window.show()
        print("   ✅ Ventana mostrada")
        
        print()
        print("🎉 TEST EXITOSO!")
        print("   La ventana debería aparecer ahora.")
        print("   Cierra la ventana para continuar.")
        print()
        
        # Ejecutar aplicación
        return app.exec_() == 0
        
    except Exception as e:
        print(f"   ❌ Error al crear ventana: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test de importaciones del proyecto POS"""
    print("\n🔍 Test de Importaciones del Proyecto")
    print("=" * 38)
    
    # Lista de módulos a probar
    modules_to_test = [
        ('models.base', 'Modelos base'),
        ('models.user', 'Modelo de usuario'),
        ('utils.database', 'Utilidades de base de datos'),
        ('controllers.app_controller', 'Controlador principal'),
        ('views.login_window', 'Ventana de login')
    ]
    
    all_imports_ok = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"   ✅ {description} ({module_name})")
        except ImportError as e:
            print(f"   ❌ {description} ({module_name}): {e}")
            all_imports_ok = False
    
    return all_imports_ok

if __name__ == "__main__":
    # Configurar path del proyecto
    import os
    from pathlib import Path
    
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    print(f"📁 Directorio del proyecto: {project_root}")
    print()
    
    # Ejecutar tests
    pyqt5_ok = test_pyqt5_basic()
    
    if pyqt5_ok:
        imports_ok = test_imports()
        
        if imports_ok:
            print("\n🎉 TODOS LOS TESTS PASARON")
            print("   La aplicación POS debería funcionar correctamente.")
            print("   Ejecutar: python main.py")
        else:
            print("\n⚠️  TEST DE PYQT5 OK, PERO HAY PROBLEMAS CON IMPORTACIONES")
            print("   Verificar que todos los archivos del proyecto estén presentes.")
    else:
        print("\n❌ TEST DE PYQT5 FALLÓ")
        print("   Soluciones sugeridas:")
        print("   1. pip install PyQt5==5.15.9")
        print("   2. Instalar Visual C++ Redistributable 2015-2019")
        print("   3. Ejecutar como administrador")
        print("   4. Deshabilitar antivirus temporalmente")
        
    input("\nPresiona Enter para salir...")
