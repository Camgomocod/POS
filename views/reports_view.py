# views/reports_view_simple.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QGridLayout, QDateEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QMessageBox, QFileDialog, QSplitter, QScrollArea, QDialog, QTabWidget)
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPainter
from utils.colors import ColorPalette
from controllers.menu_controller import MenuController
from controllers.order_controller import OrderController
from controllers.reports_controller import ReportsController

# Importación opcional de matplotlib para evitar crashes
MATPLOTLIB_AVAILABLE = True
try:
    import matplotlib
    matplotlib.use('Qt5Agg')  # Configurar backend antes de importar pyplot
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.dates as mdates
    print("✅ matplotlib cargado correctamente")
except ImportError as e:
    print(f"⚠️  matplotlib no disponible: {e}")
    MATPLOTLIB_AVAILABLE = False
    # Crear clases dummy para evitar errores
    class FigureCanvas:
        def __init__(self, *args, **kwargs):
            pass
    class Figure:
        def __init__(self, *args, **kwargs):
            pass

from datetime import datetime, timedelta
import csv
import os
import traceback

class ReportsView(QWidget):
    """Vista principal de reportes con análisis detallado integrado"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_ctrl = MenuController()
        self.order_ctrl = OrderController()
        self.reports_ctrl = ReportsController()
        self.current_mode = "main"  # "main" o "detailed"
        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        """Configurar interfaz principal de reportes"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header con título y filtros
        header_frame = self.create_header()
        layout.addWidget(header_frame)
        
        # Área principal con splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo: Métricas y filtros
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Panel derecho: Gráficos
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Configurar proporción del splitter
        splitter.setStretchFactor(0, 1)  # Panel izquierdo
        splitter.setStretchFactor(1, 3)  # Panel derecho (más grande)
        splitter.setSizes([400, 720])
            
        layout.addWidget(splitter)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
        """)

    def show_detailed_analysis(self):
        """Alternar entre vista principal y análisis detallado"""
        if self.current_mode == "main":
            self.switch_to_detailed_mode()
        else:
            self.switch_to_main_mode()

    def switch_to_detailed_mode(self):
        """Cambiar al modo de análisis detallado"""
        print("📊 Cambiando a modo detallado...")
        self.current_mode = "detailed"
        
        # Limpiar el contenido actual del panel derecho
        self.clear_right_panel_content()
        
        # Crear el contenido detallado
        detailed_content = self.create_detailed_content()
        self.right_content_layout.addWidget(detailed_content)
        
        # Actualizar el botón
        self.details_btn.setText("� Volver a Gráficos")
        print("✅ Modo detallado activado")

    def switch_to_main_mode(self):
        """Cambiar al modo principal con gráficos"""
        print("📈 Cambiando a modo principal...")
        self.current_mode = "main"
        
        # Limpiar el contenido actual del panel derecho
        self.clear_right_panel_content()
        
        # Recrear el gráfico
        charts_frame = self.create_charts_frame()
        self.right_content_layout.addWidget(charts_frame)
        
        # Actualizar el botón
        self.details_btn.setText("� Ver Análisis Detallado")
        
        # Recargar el gráfico
        self.load_sales_chart()
        print("✅ Modo principal activado")

    def clear_right_panel_content(self):
        """Limpiar el contenido del panel derecho"""
        # Eliminar todos los widgets del layout de contenido
        while self.right_content_layout.count():
            child = self.right_content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_detailed_content(self):
        """Crear el contenido del análisis detallado"""
        content_frame = QFrame()
        content_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)};
                border-radius: 8px;
                padding: 5px;
            }}
        """)
        
        layout = QVBoxLayout(content_frame)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Crear el TabWidget con las tres pestañas
        from PyQt5.QtWidgets import QTabWidget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
                background-color: {ColorPalette.PLATINUM};
                top: -1px;
            }}
            QTabBar::tab {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                padding: 10px 20px;
                margin-right: 3px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border-bottom-color: {ColorPalette.YINMN_BLUE};
                font-weight: bold;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.5)};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        
        # Pestaña 1: Productos más vendidos
        products_tab = self.create_products_analysis_tab()
        tab_widget.addTab(products_tab, "🍽️ Productos Top")
        
        # Pestaña 2: Análisis por categorías
        categories_tab = self.create_categories_analysis_tab()
        tab_widget.addTab(categories_tab, "📁 Categorías")
        
        # Pestaña 3: Análisis horario
        hours_tab = self.create_hours_analysis_tab()
        tab_widget.addTab(hours_tab, "⏰ Tendencias Horarias")
        
        layout.addWidget(tab_widget)
        
        return content_frame

    def create_products_analysis_tab(self):
        """Crear pestaña de análisis de productos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Tabla de productos con headers simplificados
        products_table = QTableWidget()
        products_table.setColumnCount(6)
        products_table.setHorizontalHeaderLabels([
            "Producto", "Cantidad Vendida", "Ingresos Totales", 
            "Precio Promedio", "Margen (%)", "Última Venta"
        ])
        
        # Estilo simplificado que GARANTIZA headers visibles
        products_table.setStyleSheet(f"""
            QTableWidget {{
                border: 2px solid {ColorPalette.YINMN_BLUE};
                border-radius: 8px;
                background-color: white;
                gridline-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
            }}
            QHeaderView::section {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: white !important;
                font-weight: bold !important;
                font-size: 12px !important;
                padding: 8px !important;
                border: none;
                text-align: center;
                min-height: 25px;
            }}
        """)
        
        # FORZAR visibilidad de headers
        products_table.horizontalHeader().setVisible(True)
        products_table.horizontalHeader().setDefaultSectionSize(120)
        products_table.horizontalHeader().setMinimumSectionSize(80)
        products_table.verticalHeader().setVisible(False)
        products_table.setAlternatingRowColors(True)
        products_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Cargar datos sin headers duplicados
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            products_data = self.reports_ctrl.get_top_products(start_date, end_date, limit=20)
            
            if products_data and len(products_data) > 0:
                products_table.setRowCount(len(products_data))
                for row, product in enumerate(products_data):
                    products_table.setItem(row, 0, QTableWidgetItem(str(product.get('name', 'N/A'))))
                    products_table.setItem(row, 1, QTableWidgetItem(str(product.get('quantity', 0))))
                    products_table.setItem(row, 2, QTableWidgetItem(f"${product.get('revenue', 0):,.0f}"))
                    products_table.setItem(row, 3, QTableWidgetItem(f"${product.get('avg_price', 0):,.0f}"))
                    products_table.setItem(row, 4, QTableWidgetItem(f"{product.get('margin', 0):.1f}%"))
                    products_table.setItem(row, 5, QTableWidgetItem(str(product.get('last_sale', 'N/A'))))
            else:
                # Datos de muestra con cálculos correctos de margen y fecha de última venta
                sample_data = [
                    {'name': 'Café Americano', 'quantity': 45, 'revenue': 180.00, 'avg_price': 4.00, 'margin': 75.0, 'last_sale': '2025-08-08'},
                    {'name': 'Cappuccino', 'quantity': 32, 'revenue': 160.00, 'avg_price': 5.00, 'margin': 80.0, 'last_sale': '2025-08-08'},
                    {'name': 'Croissant', 'quantity': 28, 'revenue': 84.00, 'avg_price': 3.00, 'margin': 66.7, 'last_sale': '2025-08-07'},
                    {'name': 'Sandwich Club', 'quantity': 18, 'revenue': 144.00, 'avg_price': 8.00, 'margin': 62.5, 'last_sale': '2025-08-08'},
                    {'name': 'Latte', 'quantity': 25, 'revenue': 137.50, 'avg_price': 5.50, 'margin': 72.7, 'last_sale': '2025-08-08'},
                ]
                
                products_table.setRowCount(len(sample_data))
                for row, product in enumerate(sample_data):
                    products_table.setItem(row, 0, QTableWidgetItem(product['name']))
                    products_table.setItem(row, 1, QTableWidgetItem(str(product['quantity'])))
                    products_table.setItem(row, 2, QTableWidgetItem(f"${product['revenue']:,.0f}"))
                    products_table.setItem(row, 3, QTableWidgetItem(f"${product['avg_price']:,.0f}"))
                    products_table.setItem(row, 4, QTableWidgetItem(f"{product['margin']:.1f}%"))
                    products_table.setItem(row, 5, QTableWidgetItem(product['last_sale']))
        except Exception as e:
            print(f"Error cargando productos: {e}")
            products_table.setRowCount(1)
            products_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
        
        products_table.resizeColumnsToContents()
        layout.addWidget(products_table)
        
        return widget

    def create_categories_analysis_tab(self):
        """Crear pestaña de análisis por categorías"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Tabla de categorías con headers simplificados
        categories_table = QTableWidget()
        categories_table.setColumnCount(5)
        categories_table.setHorizontalHeaderLabels([
            "Categoría", "Productos Vendidos", "Ingresos Totales", 
            "Promedio por Producto", "% del Total"
        ])
        
        # Estilo simplificado que GARANTIZA headers visibles
        categories_table.setStyleSheet(f"""
            QTableWidget {{
                border: 2px solid {ColorPalette.SUCCESS};
                border-radius: 8px;
                background-color: white;
                gridline-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.3)};
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.2)};
            }}
            QHeaderView::section {{
                background-color: {ColorPalette.SUCCESS};
                color: white !important;
                font-weight: bold !important;
                font-size: 12px !important;
                padding: 8px !important;
                border: none;
                text-align: center;
                min-height: 25px;
            }}
        """)
        
        # FORZAR visibilidad de headers
        categories_table.horizontalHeader().setVisible(True)
        categories_table.horizontalHeader().setDefaultSectionSize(120)
        categories_table.horizontalHeader().setMinimumSectionSize(80)
        categories_table.verticalHeader().setVisible(False)
        categories_table.setAlternatingRowColors(True)
        categories_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Cargar datos sin headers duplicados
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            categories_data = self.reports_ctrl.get_sales_by_category(start_date, end_date)
            
            if categories_data and len(categories_data) > 0:
                categories_table.setRowCount(len(categories_data))
                for row, category in enumerate(categories_data):
                    revenue = category.get('revenue', 0)
                    avg_price = revenue / category.get('total_items', 1) if category.get('total_items', 0) > 0 else 0
                    
                    categories_table.setItem(row, 0, QTableWidgetItem(str(category.get('name', 'N/A'))))
                    categories_table.setItem(row, 1, QTableWidgetItem(str(category.get('total_items', 0))))
                    categories_table.setItem(row, 2, QTableWidgetItem(f"${revenue:,.0f}"))
                    categories_table.setItem(row, 3, QTableWidgetItem(f"${avg_price:,.0f}"))
                    categories_table.setItem(row, 4, QTableWidgetItem(f"{category.get('percentage', 0):.1f}%"))
            else:
                # Datos de muestra sin headers duplicados
                sample_data = [
                    {'name': 'Bebidas Calientes', 'quantity': 102, 'revenue': 477.50, 'avg_price': 4.68, 'percentage': 42.5},
                    {'name': 'Postres', 'quantity': 45, 'revenue': 225.00, 'avg_price': 5.00, 'percentage': 20.1},
                    {'name': 'Comida Rápida', 'quantity': 38, 'revenue': 304.00, 'avg_price': 8.00, 'percentage': 27.1},
                    {'name': 'Bebidas Frías', 'quantity': 22, 'revenue': 115.50, 'avg_price': 5.25, 'percentage': 10.3},
                ]
                
                categories_table.setRowCount(len(sample_data))
                for row, category in enumerate(sample_data):
                    categories_table.setItem(row, 0, QTableWidgetItem(category['name']))
                    categories_table.setItem(row, 1, QTableWidgetItem(str(category['quantity'])))
                    categories_table.setItem(row, 2, QTableWidgetItem(f"${category['revenue']:,.0f}"))
                    categories_table.setItem(row, 3, QTableWidgetItem(f"${category['avg_price']:,.0f}"))
                    categories_table.setItem(row, 4, QTableWidgetItem(f"{category['percentage']:.1f}%"))
        except Exception as e:
            print(f"Error cargando categorías: {e}")
            categories_table.setRowCount(1)
            categories_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
        
        categories_table.resizeColumnsToContents()
        layout.addWidget(categories_table)
        
        return widget

    def create_hours_analysis_tab(self):
        """Crear pestaña de análisis horario"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Tabla de horas con headers simplificados
        hours_table = QTableWidget()
        hours_table.setColumnCount(5)
        hours_table.setHorizontalHeaderLabels([
            "Rango Horario", "Número de Órdenes", "Ingresos Totales", "Ticket Promedio", 
            "% del Total"
        ])
        
        # Estilo simplificado que GARANTIZA headers visibles
        hours_table.setStyleSheet(f"""
            QTableWidget {{
                border: 2px solid {ColorPalette.WARNING};
                border-radius: 8px;
                background-color: white;
                gridline-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.3)};
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.WARNING, 0.2)};
            }}
            QHeaderView::section {{
                background-color: {ColorPalette.WARNING};
                color: white !important;
                font-weight: bold !important;
                font-size: 12px !important;
                padding: 8px !important;
                border: none;
                text-align: center;
                min-height: 25px;
            }}
        """)
        
        # FORZAR visibilidad de headers
        hours_table.horizontalHeader().setVisible(True)
        hours_table.horizontalHeader().setDefaultSectionSize(120)
        hours_table.horizontalHeader().setMinimumSectionSize(80)
        hours_table.verticalHeader().setVisible(False)
        hours_table.setAlternatingRowColors(True)
        hours_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Cargar datos sin headers duplicados
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            hours_data = self.reports_ctrl.get_sales_by_hour(start_date, end_date)
            
            if hours_data and len(hours_data) > 0:
                hours_table.setRowCount(len(hours_data))
                for row, hour in enumerate(hours_data):
                    hours_table.setItem(row, 0, QTableWidgetItem(hour.get('hour_range', 'N/A')))
                    hours_table.setItem(row, 1, QTableWidgetItem(str(hour.get('order_count', 0))))
                    hours_table.setItem(row, 2, QTableWidgetItem(f"${hour.get('total_sales', 0):,.0f}"))
                    hours_table.setItem(row, 3, QTableWidgetItem(f"${hour.get('avg_ticket', 0):,.0f}"))
                    hours_table.setItem(row, 4, QTableWidgetItem(f"{hour.get('percentage', 0):.1f}%"))
            else:
                # Datos de muestra sin headers duplicados
                sample_data = [
                    {'hour_range': '08:00-09:00', 'order_count': 12, 'total_sales': 62.50, 'avg_ticket': 5.21, 'percentage': 5.2},
                    {'hour_range': '09:00-10:00', 'order_count': 28, 'total_sales': 142.00, 'avg_ticket': 5.07, 'percentage': 11.8},
                    {'hour_range': '10:00-11:00', 'order_count': 45, 'total_sales': 234.75, 'avg_ticket': 5.22, 'percentage': 19.6},
                    {'hour_range': '11:00-12:00', 'order_count': 38, 'total_sales': 198.50, 'avg_ticket': 5.22, 'percentage': 16.5},
                    {'hour_range': '12:00-13:00', 'order_count': 52, 'total_sales': 286.00, 'avg_ticket': 5.50, 'percentage': 23.8},
                    {'hour_range': '13:00-14:00', 'order_count': 41, 'total_sales': 225.50, 'avg_ticket': 5.50, 'percentage': 18.8},
                    {'hour_range': '14:00-15:00', 'order_count': 33, 'total_sales': 171.50, 'avg_ticket': 5.20, 'percentage': 14.3},
                ]
                
                hours_table.setRowCount(len(sample_data))
                for row, hour in enumerate(sample_data):
                    hours_table.setItem(row, 0, QTableWidgetItem(hour['hour_range']))
                    hours_table.setItem(row, 1, QTableWidgetItem(str(hour['order_count'])))
                    hours_table.setItem(row, 2, QTableWidgetItem(f"${hour['total_sales']:,.0f}"))
                    hours_table.setItem(row, 3, QTableWidgetItem(f"${hour['avg_ticket']:,.0f}"))
                    hours_table.setItem(row, 4, QTableWidgetItem(f"{hour['percentage']:.1f}%"))
        except Exception as e:
            print(f"Error cargando datos horarios: {e}")
            hours_table.setRowCount(1)
            hours_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
        
        hours_table.resizeColumnsToContents()
        layout.addWidget(hours_table)
        
        return widget

    def create_header(self):
        """Crear header con título y controles principales"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 5px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                padding: 5px;
            }}
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        title_layout = QVBoxLayout()
        title_label = QLabel("📊 Reportes de Negocio")
        title_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        title_layout.addWidget(title_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Filtros de fecha
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(5)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setStyleSheet(self.get_date_edit_style())
        self.start_date.dateChanged.connect(self.refresh_data)
        filters_layout.addWidget(self.start_date)
        
        # Fecha fin
        filters_layout.addWidget(QLabel("Hasta:"))
        
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet(self.get_date_edit_style())
        self.end_date.dateChanged.connect(self.refresh_data)
        filters_layout.addWidget(self.end_date)
        
        # Botón actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 4px 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        refresh_btn.clicked.connect(self.refresh_data)
        filters_layout.addWidget(refresh_btn)
        
        layout.addLayout(filters_layout)
        
        return header_frame

    def create_left_panel(self):
        """Crear panel izquierdo con métricas clave y controles"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 10px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        # Usar scroll para pantallas pequeñas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        
        # Métricas principales en grid compacto 2x2
        metrics_frame = QFrame()
        metrics_layout = QGridLayout(metrics_frame)
        metrics_layout.setSpacing(8)
        metrics_layout.setContentsMargins(0, 10, 0, 10)
        
        self.sales_metric = self.create_compact_metric_widget("💰", "Ventas", "$0.00", ColorPalette.SUCCESS)
        self.orders_metric = self.create_compact_metric_widget("📋", "Órdenes", "0", ColorPalette.YINMN_BLUE)
        self.avg_ticket_metric = self.create_compact_metric_widget("🎯", "Promedio", "$0.00", ColorPalette.WARNING)
        self.margin_metric = self.create_compact_metric_widget("📊", "Margen", "0%", ColorPalette.ERROR)
        
        metrics_layout.addWidget(self.sales_metric, 0, 0)
        metrics_layout.addWidget(self.orders_metric, 0, 1)
        metrics_layout.addWidget(self.avg_ticket_metric, 1, 0)
        metrics_layout.addWidget(self.margin_metric, 1, 1)
        
        layout.addWidget(metrics_frame)
        
        # Período rápido compacto
        period_frame = QFrame()
        period_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        period_layout = QVBoxLayout(period_frame)
        period_layout.setSpacing(6)
        
        period_title = QLabel("⚡ Períodos Rápidos")
        period_title.setStyleSheet("font-weight: bold; font-size: 12px; margin-bottom: 5px;")
        period_layout.addWidget(period_title)
        
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(4)
        
        today_btn = QPushButton("📅 Hoy")
        week_btn = QPushButton("📆 Semana")
        month_btn = QPushButton("🗓️ Mes")
        
        buttons_layout.addWidget(today_btn, 0, 0)
        buttons_layout.addWidget(week_btn, 0, 1)
        buttons_layout.addWidget(month_btn, 0, 2)
        
        today_btn.clicked.connect(lambda: self.set_quick_period("today"))
        week_btn.clicked.connect(lambda: self.set_quick_period("week"))
        month_btn.clicked.connect(lambda: self.set_quick_period("month"))
        
        button_style = f"""
            QPushButton {{
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                padding: 6px 4px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
                text-align: center;
                min-height: 25px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
            }}
        """
        
        for btn in [today_btn, week_btn, month_btn]:
            btn.setStyleSheet(button_style)
        
        period_layout.addLayout(buttons_layout)
        layout.addWidget(period_frame)
        
        # Sección de acciones
        actions_frame = QFrame()
        actions_frame.setStyleSheet("background-color: transparent; border: none;")
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(0, 10, 0, 0)
        actions_layout.setSpacing(8)

        export_btn = QPushButton("📤 Exportar Datos")
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        export_btn.clicked.connect(self.export_data)
        actions_layout.addWidget(export_btn)
        
        layout.addWidget(actions_frame)
        layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.addWidget(scroll_area)
        
        return panel

    def create_right_panel(self):
        """Crear panel derecho con gráficos expandidos"""
        self.right_panel = QFrame()
        self.right_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 10px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        layout = QVBoxLayout(self.right_panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header con título y botón de detalles
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📈 Análisis de Ventas")
        title_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botón para mostrar vista detallada
        self.details_btn = QPushButton("📊 Ver Análisis Detallado")
        self.details_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        self.details_btn.clicked.connect(self.show_detailed_analysis)
        header_layout.addWidget(self.details_btn)
        
        layout.addLayout(header_layout)
        
        # Contenedor para el contenido que puede cambiar (gráficos o análisis detallado)
        self.right_content_frame = QFrame()
        self.right_content_layout = QVBoxLayout(self.right_content_frame)
        self.right_content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear gráficos iniciales
        charts_frame = self.create_charts_frame()
        self.right_content_layout.addWidget(charts_frame)
        
        layout.addWidget(self.right_content_frame)
        
        return self.right_panel

    def create_charts_frame(self):
        """Crear frame con gráficos"""
        charts_frame = QFrame()
        charts_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        charts_layout = QVBoxLayout(charts_frame)
        charts_layout.setContentsMargins(5, 5, 5, 5)
        
        # Gráfico de ventas diarias expandido
        self.sales_chart = self.create_sales_chart()
        charts_layout.addWidget(self.sales_chart)
        
        return charts_frame

    def create_compact_metric_widget(self, icon, title, value, color):
        """Crear widget de métrica compacto para pantallas pequeñas"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(color, 0.1)};
                border: 1px solid {ColorPalette.with_alpha(color, 0.3)};
                border-left: 3px solid {color};
                border-radius: 6px;
                padding: 8px;
                min-height: 20px;
                max-height: 90px;
                margin: 4px 0px 4px 0px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(2)
        
        # Header con icono y título en una línea
        header_layout = QHBoxLayout()
        header_layout.setSpacing(4)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 12px;
            color: {color};
            min-width: 20px;
            max-height: 20px;
            
        """)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 10px;
            font-weight: bold;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.8)};
            min-width: 100px;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valor
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {color};
            text-align: center;
            max-height: 250px;
            margin-top: 4px;
        """)
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        # Guardar referencia al label de valor para actualizaciones
        widget.value_label = value_label
        
        return widget

    def create_sales_chart(self):
        """Crear gráfico de ventas diarias expandido"""
        # Crear figura de matplotlib más grande para aprovechar el espacio
        self.figure = Figure(figsize=(10, 4), dpi=100, facecolor='#F7F9FC')
        self.canvas = FigureCanvas(self.figure)
        
        # Aplicar estilo
        self.canvas.setStyleSheet(f"""
            FigureCanvas {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 8px;
                min-height: 400px;
            }}
        """)
        
        return self.canvas

    def get_date_edit_style(self):
        """Obtener estilo para QDateEdit"""
        return f"""
            QDateEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 11px;
                color: {ColorPalette.RICH_BLACK};
                min-width: 90px;
                max-height: 28px;
            }}
            QDateEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """

    def set_quick_period(self, period):
        """Establecer período rápido"""
        today = QDate.currentDate()
        
        if period == "today":
            self.start_date.setDate(today)
            self.end_date.setDate(today)
        elif period == "week":
            days_since_monday = today.dayOfWeek() - 1
            monday = today.addDays(-days_since_monday)
            self.start_date.setDate(monday)
            self.end_date.setDate(today)
        elif period == "month":
            first_day = QDate(today.year(), today.month(), 1)
            self.start_date.setDate(first_day)
            self.end_date.setDate(today)
        
        self.refresh_data()

    def load_initial_data(self):
        """Cargar datos iniciales"""
        self.refresh_data()

    def refresh_data(self):
        """Actualizar todos los datos"""
        try:
            self.load_metrics()
            self.load_sales_chart()
        except Exception as e:
            print(f"Error en refresh_data: {e}")

    def load_metrics(self):
        """Cargar métricas principales"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            sales_summary = self.reports_ctrl.get_sales_summary(start_date, end_date)
            
            if sales_summary and isinstance(sales_summary, dict):
                total_sales = sales_summary.get('total_sales', 0.0)
                total_orders = sales_summary.get('total_orders', 0)
                avg_ticket = sales_summary.get('avg_ticket', 0.0)
                
                try:
                    margin_data = self.reports_ctrl.get_profit_margin_analysis(start_date, end_date)
                    overall_margin = margin_data.get('overall_margin', 0.0) if margin_data else 0.0
                except:
                    overall_margin = 0.0
                
                self.sales_metric.value_label.setText(f"${total_sales:,.0f}")
                self.orders_metric.value_label.setText(str(total_orders))
                self.avg_ticket_metric.value_label.setText(f"${avg_ticket:,.0f}")
                self.margin_metric.value_label.setText(f"{overall_margin:.1f}%")
            else:
                self.sales_metric.value_label.setText("$0.00")
                self.orders_metric.value_label.setText("0")
                self.avg_ticket_metric.value_label.setText("$0.00")
                self.margin_metric.value_label.setText("0.0%")
            
        except Exception as e:
            print(f"Error cargando métricas: {e}")
            self.sales_metric.value_label.setText("Error")
            self.orders_metric.value_label.setText("Error")
            self.avg_ticket_metric.value_label.setText("Error")
            self.margin_metric.value_label.setText("Error")

    def load_sales_chart(self):
        """Cargar gráfico de ventas"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from matplotlib.colors import LinearSegmentedColormap
            import numpy as np
            
            self.figure.clear()
            # Configurar estilo moderno
            plt.style.use('default')
            
            # Crear subplot con fondo personalizado
            ax = self.figure.add_subplot(111, facecolor='#F7F9FC')
            
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Verificar si es un solo día para mostrar datos horarios
            is_single_day = start_date == end_date
            
            if is_single_day:
                # Usar datos horarios para un solo día
                hourly_data = self.reports_ctrl.get_sales_by_hour(start_date, end_date)
                
                if hourly_data and len(hourly_data) > 0:
                    hours = [item['hour_range'] for item in hourly_data]
                    sales = [float(item['total_sales']) for item in hourly_data]
                    
                    # Colores modernos para vista horaria
                    line_color = '#DC2626'  # Rojo para distinguir de vista diaria
                    
                    # Crear posiciones numéricas para las horas
                    x_positions = list(range(len(hours)))
                    
                    # Línea principal con puntos
                    ax.plot(x_positions, sales, 
                           color=line_color, 
                           linewidth=3, 
                           marker='o', 
                           markersize=8, 
                           markerfacecolor='#B91C1C',
                           markeredgecolor='white',
                           markeredgewidth=2,
                           alpha=0.9,
                           zorder=3)
                    
                    # Área sombreada
                    ax.fill_between(x_positions, sales, 0, 
                                   alpha=0.6, 
                                   color='#EF4444',
                                   zorder=1)
                    
                    # Área adicional para efecto de profundidad
                    ax.fill_between(x_positions, sales, 0, 
                                   alpha=0.3, 
                                   color='#FCA5A5',
                                   zorder=0)
                    
                    # Configurar etiquetas del eje X con horas
                    ax.set_xticks(x_positions)
                    ax.set_xticklabels(hours, rotation=45, ha='right')
                    
                    # Configurar límites
                    max_sales = max(sales) if sales else 0
                    if max_sales > 0:
                        ax.set_ylim(0, max_sales * 1.1)
                    
                    # Añadir líneas de valor promedio
                    avg_sales = sum(sales) / len(sales) if sales else 0
                    ax.axhline(y=avg_sales, color='#F59E0B', linestyle='--', alpha=0.7, linewidth=2, label=f'Promedio: ${avg_sales:.2f}')
                    
                    # Título específico para vista horaria
                    ax.text(0.02, 0.98, f'Ventas por Horas - {start_date.strftime("%d/%m/%Y")}', 
                           transform=ax.transAxes, fontsize=12, fontweight='bold',
                           verticalalignment='top', color='#374151',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
                    
                else:
                    ax.text(0.5, 0.5, f'No hay ventas registradas para hoy\n{start_date.strftime("%d/%m/%Y")}\n\nPrueba con otro día', 
                           ha='center', va='center', transform=ax.transAxes,
                           fontsize=14, color='#6B7280', 
                           bbox=dict(boxstyle="round,pad=0.5", facecolor='#F3F4F6', alpha=0.8))
            else:
                # Usar datos diarios para períodos más largos
                daily_sales = self.reports_ctrl.get_daily_sales(start_date, end_date)
                
                if daily_sales and len(daily_sales) > 0:
                    dates = []
                    sales = []
                    
                    for item in daily_sales:
                        if isinstance(item['date'], str):
                            date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                        else:
                            date_obj = item['date']
                        
                        dates.append(date_obj)
                        sales.append(float(item['total_sales']))
                    
                    # Colores modernos y gradientes para vista diaria
                    line_color = '#2563EB'  # Azul moderno
                    
                    # Crear gradiente para el área
                    y_max = max(sales) if sales else 100
                    
                    # Línea principal con sombra
                    ax.plot(dates, sales, 
                           color=line_color, 
                           linewidth=3, 
                           marker='o', 
                           markersize=8, 
                           markerfacecolor='#1D4ED8',
                           markeredgecolor='white',
                           markeredgewidth=2,
                           alpha=0.9,
                           zorder=3)
                    
                    # Área sombreada con gradiente
                    ax.fill_between(dates, sales, 0, 
                                   alpha=0.6, 
                                   color='#3B82F6',
                                   zorder=1)
                    
                    # Área adicional para efecto de profundidad
                    ax.fill_between(dates, sales, 0, 
                                   alpha=0.3, 
                                   color='#60A5FA',
                                   zorder=0)
                    
                    # Configurar formato de fechas
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//7)))
                    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
                    
                    # Configurar límites
                    max_sales = max(sales) if sales else 0
                    if max_sales > 0:
                        ax.set_ylim(0, max_sales * 1.1)
                    
                    # Añadir líneas de valor promedio
                    avg_sales = sum(sales) / len(sales) if sales else 0
                    ax.axhline(y=avg_sales, color='#F59E0B', linestyle='--', alpha=0.7, linewidth=2, label=f'Promedio: ${avg_sales:.2f}')
                    
                else:
                    ax.text(0.5, 0.5, 'No hay datos para el período seleccionado\n\nPrueba con otro rango de fechas', 
                           ha='center', va='center', transform=ax.transAxes,
                           fontsize=14, color='#6B7280', 
                           bbox=dict(boxstyle="round,pad=0.5", facecolor='#F3F4F6', alpha=0.8))
            
            # Grid moderno (sin títulos de ejes para máximo espacio)
            ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color='#D1D5DB')
            ax.set_axisbelow(True)
            
            # Estilo de los ejes
            ax.tick_params(axis='both', which='major', labelsize=10, colors='#4B5563')
            ax.tick_params(axis='x', which='major', pad=8)
            ax.tick_params(axis='y', which='major', pad=8)
            
            # Remover spines superiores y derechos para look más limpio
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#D1D5DB')
            ax.spines['bottom'].set_color('#D1D5DB')
            
            # Formato de números en Y con separadores de miles
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Leyenda si hay datos
            if (is_single_day and hourly_data and len(hourly_data) > 0) or (not is_single_day and daily_sales and len(daily_sales) > 0):
                ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, 
                         framealpha=0.9, facecolor='white', edgecolor='#D1D5DB')
            
            # Ajuste automático del layout
            self.figure.tight_layout(pad=2.0)
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error cargando gráfico de ventas: {e}")
            self.figure.clear()
            ax = self.figure.add_subplot(111, facecolor='#FEF2F2')
            ax.text(0.5, 0.5, f'Error cargando datos:\n\n{str(e)}', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12, color='#DC2626',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='#FECACA', alpha=0.8))
            ax.axis('off')
            self.canvas.draw()

    def export_data(self):
        """Exportar datos a CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Reportes",
                f"reportes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV files (*.csv)"
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Información del reporte
                    writer.writerow(["Reporte de Ventas"])
                    writer.writerow(["Período:", f"{self.start_date.date().toString()} - {self.end_date.date().toString()}"])
                    writer.writerow(["Generado:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    writer.writerow([])
                    
                    # Métricas principales
                    writer.writerow(["Métricas Principales"])
                    writer.writerow(["Ventas Totales:", self.sales_metric.value_label.text()])
                    writer.writerow(["Órdenes Totales:", self.orders_metric.value_label.text()])
                    writer.writerow(["Ticket Promedio:", self.avg_ticket_metric.value_label.text()])
                    writer.writerow(["Margen:", self.margin_metric.value_label.text()])
                
                QMessageBox.information(self, "Exportación Exitosa", f"Datos exportados a:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar datos:\n{str(e)}")
