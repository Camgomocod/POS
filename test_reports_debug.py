#!/usr/bin/env python3
# Test debugging para la vista de reportes

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from views.reports_view import ReportsView

def test_reports_view():
    """Test debug de la vista de reportes"""
    
    app = QApplication(sys.argv)
    
    # Crear ventana principal
    main_window = QMainWindow()
    main_window.setWindowTitle("Test Debug - Reports View")
    main_window.resize(1200, 800)
    
    # Crear la vista de reportes
    print("📊 Creando vista de reportes...")
    reports_view = ReportsView()
    
    # Establecer como widget central
    main_window.setCentralWidget(reports_view)
    
    # Debug: Mostrar valores después de la inicialización
    def debug_after_init():
        print("🔍 DEBUG después de inicialización:")
        print(f"  Start date: {reports_view.start_date.date().toString()}")
        print(f"  End date: {reports_view.end_date.date().toString()}")
        print(f"  Ventas metric: {reports_view.sales_metric.value_label.text()}")
        print(f"  Órdenes metric: {reports_view.orders_metric.value_label.text()}")
        print(f"  Promedio metric: {reports_view.avg_ticket_metric.value_label.text()}")
        print(f"  Margen metric: {reports_view.margin_metric.value_label.text()}")
        
        # Probar refresh manual
        print("🔄 Ejecutando refresh manual...")
        reports_view.refresh_data()
        
        # Mostrar valores después del refresh
        QTimer.singleShot(1000, lambda: print_final_values(reports_view))
    
    def print_final_values(view):
        print("✅ VALORES FINALES:")
        print(f"  Ventas: {view.sales_metric.value_label.text()}")
        print(f"  Órdenes: {view.orders_metric.value_label.text()}")
        print(f"  Promedio: {view.avg_ticket_metric.value_label.text()}")
        print(f"  Margen: {view.margin_metric.value_label.text()}")
        print("📈 Vista lista para usar!")
    
    # Ejecutar debug después de que la vista esté completamente inicializada
    QTimer.singleShot(500, debug_after_init)
    
    # Mostrar ventana
    main_window.show()
    
    print("🚀 Vista de reportes cargada. Presiona Ctrl+C para salir.")
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\n👋 Cerrando aplicación...")
        app.quit()

if __name__ == "__main__":
    test_reports_view()
