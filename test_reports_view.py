#!/usr/bin/env python3
"""
Prueba rápida de la vista de reportes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow
from views.reports_view import ReportsView

class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba - Vista de Reportes")
        self.setGeometry(100, 100, 1200, 800)
        
        # Crear vista de reportes
        self.reports_view = ReportsView(self)
        self.setCentralWidget(self.reports_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        window = TestMainWindow()
        window.show()
        
        print("✅ Vista de reportes cargada exitosamente")
        print("🔍 Puedes probar el botón 'Ver Tablas Detalladas' en el panel izquierdo")
        print("📊 O el botón 'Ver Análisis Detallado' en el panel derecho")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error al cargar la vista: {e}")
        import traceback
        traceback.print_exc()
