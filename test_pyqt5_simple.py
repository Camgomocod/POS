#!/usr/bin/env python3
"""
Prueba simple de PyQt5 para verificar que funciona antes del sistema completo
"""

import sys
import os

def main():
    print("🧪 Prueba Simple de PyQt5")
    print("=" * 50)
    
    # Configurar entorno antes de importar PyQt5
    os.environ['QT_QPA_PLATFORM'] = 'windows'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'
    os.environ['QT_SCALE_FACTOR'] = '1'
    
    try:
        print("📍 Paso 1: Importando PyQt5...")
        from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton
        from PyQt5.QtCore import Qt
        print("✅ PyQt5 importado correctamente")
        
        print("📍 Paso 2: Creando aplicación...")
        app = QApplication(sys.argv)
        
        # Configurar aplicación
        app.setAttribute(Qt.AA_EnableHighDpiScaling, False)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, False)
        
        print("✅ Aplicación creada")
        
        print("📍 Paso 3: Creando ventana de prueba...")
        
        # Crear ventana simple
        window = QWidget()
        window.setWindowTitle("✅ Prueba PyQt5 - Sistema POS")
        window.setGeometry(300, 300, 400, 200)
        
        layout = QVBoxLayout()
        
        # Agregar elementos
        label = QLabel("🎉 ¡PyQt5 funciona correctamente!")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        
        button = QPushButton("✅ Continuar al Sistema POS")
        button.clicked.connect(window.close)
        
        layout.addWidget(label)
        layout.addWidget(button)
        
        window.setLayout(layout)
        
        print("✅ Ventana creada")
        
        print("📍 Paso 4: Mostrando ventana...")
        window.show()
        
        print("✅ ¡Prueba exitosa! Si ves la ventana, PyQt5 funciona.")
        print("💡 Ahora puedes ejecutar el sistema completo.")
        
        # Ejecutar aplicación
        app.exec_()
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando PyQt5: {e}")
        print("💡 Solución: pip install PyQt5==5.15.9")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("💡 Solución: Ejecutar fix_access_violation.bat")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPresiona Enter para salir...")
        sys.exit(1)
