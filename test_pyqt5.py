#!/usr/bin/env python3
"""
Test básico de PyQt5 para diagnosticar problemas en Windows
"""

import sys
import os

def test_basic_imports():
    """Probar importaciones básicas"""
    print("🔍 Probando importaciones básicas...")
    
    try:
        import sys
        print(f"✅ sys: {sys.version}")
    except Exception as e:
        print(f"❌ sys: {e}")
        return False
        
    try:
        import os
        print(f"✅ os: disponible")
    except Exception as e:
        print(f"❌ os: {e}")
        return False
        
    return True

def test_pyqt5_import():
    """Probar importación de PyQt5"""
    print("\n🔍 Probando importación de PyQt5...")
    
    try:
        import PyQt5
        print(f"✅ PyQt5: {PyQt5.Qt.QT_VERSION_STR}")
    except Exception as e:
        print(f"❌ PyQt5: {e}")
        return False
        
    try:
        from PyQt5.QtWidgets import QApplication
        print("✅ QApplication: importación exitosa")
    except Exception as e:
        print(f"❌ QApplication: {e}")
        return False
        
    try:
        from PyQt5.QtCore import Qt
        print("✅ QtCore: importación exitosa")
    except Exception as e:
        print(f"❌ QtCore: {e}")
        return False
        
    return True

def test_qapplication_creation():
    """Probar creación de QApplication"""
    print("\n🔍 Probando creación de QApplication...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        
        # Verificar si ya existe una instancia
        app = QApplication.instance()
        if app is None:
            print("📱 Creando nueva instancia de QApplication...")
            app = QApplication(sys.argv)
            created_new = True
        else:
            print("📱 Usando instancia existente de QApplication...")
            created_new = False
            
        print("✅ QApplication: creación exitosa")
        
        # Probar configuraciones básicas
        app.setApplicationName("Test POS")
        print("✅ setApplicationName: funciona")
        
        # Limpiar si creamos nueva instancia
        if created_new:
            app.quit()
            
        return True
        
    except Exception as e:
        print(f"❌ QApplication: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_widget():
    """Probar creación de widget simple"""
    print("\n🔍 Probando creación de widget simple...")
    
    try:
        from PyQt5.QtWidgets import QApplication, QLabel
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            created_new = True
        else:
            created_new = False
            
        # Crear widget simple
        label = QLabel("Test PyQt5")
        label.show()
        print("✅ QLabel: creación y show exitosos")
        
        # No ejecutar el loop, solo probar creación
        label.close()
        
        if created_new:
            app.quit()
            
        return True
        
    except Exception as e:
        print(f"❌ Widget simple: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment():
    """Probar variables de entorno importantes"""
    print("\n🔍 Verificando entorno...")
    
    # Variables importantes para PyQt5 en Windows
    important_vars = [
        'DISPLAY',
        'QT_QPA_PLATFORM',
        'QT_PLUGIN_PATH',
        'PATH'
    ]
    
    for var in important_vars:
        value = os.environ.get(var, 'No definida')
        print(f"📋 {var}: {value}")
    
    # Verificar Python executable
    print(f"🐍 Python executable: {sys.executable}")
    print(f"🐍 Python version: {sys.version}")
    
    return True

def main():
    """Función principal de testing"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              TEST PYQT5 - DIAGNÓSTICO WINDOWS           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    tests = [
        ("Importaciones básicas", test_basic_imports),
        ("Importación PyQt5", test_pyqt5_import),
        ("Creación QApplication", test_qapplication_creation),
        ("Widget simple", test_simple_widget),
        ("Entorno", test_environment)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Ejecutando: {test_name}")
        print("-" * 50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error inesperado en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS:")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status:10} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("\n🎉 ¡Todas las pruebas pasaron! PyQt5 debería funcionar.")
        print("💡 Si main.py aún no funciona, el problema podría ser específico del código.")
    else:
        print(f"\n⚠️  {len(results) - passed} pruebas fallaron.")
        print("💡 Revisar instalación de PyQt5 o problemas de entorno gráfico.")
    
    print("\n💻 Para más ayuda:")
    print("   - Ejecutar: diagnostico_sistema.bat")
    print("   - Verificar: pip list | findstr PyQt5")
    print("   - Reinstalar: pip install --force-reinstall PyQt5")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para continuar...")
