#!/usr/bin/env python3
# test_compact_printer_ui.py
"""
Script para probar la nueva interfaz compacta de configuración de impresoras
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from views.printer_config_view import PrinterConfigView

def test_compact_ui():
    """Probar la nueva interfaz compacta"""
    print("🖨️ Probando interfaz compacta de configuración de impresoras...")
    
    app = QApplication(sys.argv)
    
    # Crear ventana de configuración
    config_window = PrinterConfigView()
    config_window.setWindowTitle("🖨️ Configuración de Impresora Térmica - Interfaz Compacta")
    config_window.resize(900, 600)  # Tamaño optimizado para layout de columnas
    config_window.show()
    
    print("✅ Interfaz compacta cargada exitosamente")
    print("📋 Características de la nueva interfaz:")
    print("   • Layout en 2 columnas: Configuración (izquierda) | Tabla (derecha)")
    print("   • Headers más pequeños (18px → 13px)")
    print("   • Botones compactos con iconos")
    print("   • Tabla optimizada para el espacio")
    print("   • Configuración avanzada en una sola fila")
    print("   • Espaciado reducido para mejor aprovechamiento")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_compact_ui()
