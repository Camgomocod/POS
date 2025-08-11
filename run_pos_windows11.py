#!/usr/bin/env python3
"""
Script mejorado para ejecutar POS en Windows 11
Configuración especial para evitar problemas con PyQtGraph
"""

import sys
import os

def configure_for_windows11():
    """Configurar entorno específicamente para Windows 11"""
    
    # 1. Configuraciones de Qt para Windows 11
    os.environ['QT_QPA_PLATFORM'] = 'windows'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_SCALE_FACTOR'] = '1'
    
    # 2. Forzar software rendering para evitar problemas de OpenGL
    os.environ['QT_OPENGL'] = 'software'
    os.environ['QT_QUICK_BACKEND'] = 'software'
    os.environ['QT_ANGLE_PLATFORM'] = 'software'
    
    # 3. Configuraciones específicas para PyQtGraph
    os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'
    os.environ['PYQTGRAPH_USE_OPENGL'] = 'False'
    
    # 4. Configuraciones de proceso para estabilidad
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*.debug=false'
    
    print("🔧 Configuración de Windows 11 aplicada")

def main():
    print("🚀 POS SISTEMA PARA WINDOWS 11")
    print("=" * 40)
    
    # Configurar entorno para Windows 11
    configure_for_windows11()
    
    # Agregar directorio del proyecto al path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_dir)
    
    # Información del sistema
    print(f"📂 Directorio del proyecto: {project_dir}")
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Plataforma: {sys.platform}")
    
    # Verificaciones previas
    print("\n🔍 Verificaciones previas...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        print("   ✅ PyQt5 disponible")
    except ImportError as e:
        print(f"   ❌ PyQt5 no disponible: {e}")
        print("   💡 Instalar con: pip install PyQt5")
        return 1
    
    try:
        import pyqtgraph
        print("   ✅ PyQtGraph disponible")
    except ImportError as e:
        print(f"   ⚠️  PyQtGraph no disponible: {e}")
        print("   💡 Se usarán gráficos de respaldo")
    
    # Ejecutar aplicación principal
    print("\n🚀 Iniciando aplicación POS...")
    print("💡 Para salir use Ctrl+C o cierre la ventana")
    print("-" * 40)
    
    try:
        # Importar y ejecutar main
        import main
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
        return 0
    except Exception as e:
        print(f"\n❌ Error ejecutando aplicación: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
