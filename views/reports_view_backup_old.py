# views/reports_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QGridLayout, QDateEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QMessageBox, QFileDialog, QSplitter, QScrollArea, QTabWidget, QStackedWidget)
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPainter
from utils.colors import ColorPalette
from controllers.menu_controller import MenuController
from controllers.order_controller import OrderController
from controllers.reports_controller import ReportsController
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import csv
import os
import traceback

class ReportsView(QWidget):
    """Vista principal de reportes con análisis integrado"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_ctrl = MenuController()
        self.order_ctrl = OrderController()
        self.reports_ctrl = ReportsController()
        self.current_view = "main"  # "main" o "detailed"
        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        """Configurar interfaz principal de reportes con vistas integradas"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header con título y filtros (siempre visible)
        header_frame = self.create_header()
        layout.addWidget(header_frame)
        
        # Crear QStackedWidget para manejar las diferentes vistas
        self.stacked_widget = QStackedWidget()
        
        # Vista principal: Dashboard con métricas y gráfico
        main_view = self.create_main_view()
        self.stacked_widget.addWidget(main_view)
        
        # Vista detallada: Análisis con tablas
        detailed_view = self.create_detailed_view()
        self.stacked_widget.addWidget(detailed_view)
        
        layout.addWidget(self.stacked_widget)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
        """)

    def create_main_view(self):
        """Crear vista principal con métricas y gráfico"""
        main_widget = QWidget()
        
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
        splitter.setSizes([280, 840])
        
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        
        return main_widget

    def create_detailed_view(self):
        """Crear vista detallada con análisis de tablas"""
        detailed_widget = QWidget()
        layout = QVBoxLayout(detailed_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Botón para volver a la vista principal
        back_layout = QHBoxLayout()
        back_btn = QPushButton("⬅️ Volver al Dashboard")
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        back_btn.clicked.connect(self.show_main_view)
        back_layout.addWidget(back_btn)
        back_layout.addStretch()
        layout.addLayout(back_layout)
        
        # Pestañas para diferentes análisis
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                background-color: {ColorPalette.PLATINUM};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                color: {ColorPalette.RICH_BLACK};
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
            }}
            QTabBar::tab:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.7)};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        
        # Pestaña 1: Productos más vendidos
        products_tab = self.create_products_analysis_tab()
        self.tab_widget.addTab(products_tab, "🍽️ Productos Top")
        
        # Pestaña 2: Análisis por categorías
        categories_tab = self.create_categories_analysis_tab()
        self.tab_widget.addTab(categories_tab, "📁 Categorías")
        
        # Pestaña 3: Análisis horario
        hours_tab = self.create_hours_analysis_tab()
        self.tab_widget.addTab(hours_tab, "⏰ Tendencias Horarias")
        
        layout.addWidget(self.tab_widget)
        
        return detailed_widget

    def show_main_view(self):
        """Mostrar vista principal"""
        self.current_view = "main"
        self.stacked_widget.setCurrentIndex(0)
        print("✅ Cambiado a vista principal")

    def show_detailed_analysis(self):
        """Mostrar análisis detallado en el mismo placeholder"""
        print("📊 Cambiando a vista de análisis detallado...")
        self.current_view = "detailed"
        self.stacked_widget.setCurrentIndex(1)
        
        # Cargar datos en las tablas
        self.load_detailed_data()
        print("✅ Vista de análisis detallado cargada")

    def load_detailed_data(self):
        """Cargar datos para las tablas de análisis detallado"""
        try:
            # Cargar datos de productos
            self.load_products_table()
            # Cargar datos de categorías  
            self.load_categories_table()
            # Cargar datos de horas
            self.load_hours_table()
        except Exception as e:
            print(f"Error cargando datos detallados: {e}")

    def create_products_analysis_tab(self, start_date_widget, end_date_widget):
        """Crear pestaña de análisis de productos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tabla de productos
        products_table = QTableWidget()
        products_table.setColumnCount(6)
        products_table.setHorizontalHeaderLabels([
            "Producto", "Cantidad Vendida", "Ingresos Totales", 
            "Precio Promedio", "Margen (%)", "Última Venta"
        ])
        
        # Cargar datos
        try:
            start_date = start_date_widget.date().toPyDate()
            end_date = end_date_widget.date().toPyDate()
            
            products_data = self.reports_ctrl.get_top_products(start_date, end_date, limit=20)
            
            if products_data and len(products_data) > 0:
                products_table.setRowCount(len(products_data))
                for row, product in enumerate(products_data):
                    products_table.setItem(row, 0, QTableWidgetItem(str(product.get('name', 'N/A'))))
                    products_table.setItem(row, 1, QTableWidgetItem(str(product.get('quantity', 0))))
                    products_table.setItem(row, 2, QTableWidgetItem(f"${product.get('revenue', 0):.2f}"))
                    products_table.setItem(row, 3, QTableWidgetItem(f"${product.get('avg_price', 0):.2f}"))
                    products_table.setItem(row, 4, QTableWidgetItem(f"{product.get('margin', 0):.1f}%"))
                    products_table.setItem(row, 5, QTableWidgetItem(str(product.get('last_sale', 'N/A'))))
            else:
                # Datos de muestra
                sample_data = [
                    {'name': 'Café Americano', 'quantity': 45, 'revenue': 180.00, 'avg_price': 4.00, 'margin': 75.5, 'last_sale': '2025-08-08'},
                    {'name': 'Cappuccino', 'quantity': 32, 'revenue': 160.00, 'avg_price': 5.00, 'margin': 80.2, 'last_sale': '2025-08-08'},
                    {'name': 'Croissant', 'quantity': 28, 'revenue': 84.00, 'avg_price': 3.00, 'margin': 65.8, 'last_sale': '2025-08-07'},
                    {'name': 'Sandwich Club', 'quantity': 18, 'revenue': 144.00, 'avg_price': 8.00, 'margin': 55.3, 'last_sale': '2025-08-08'},
                    {'name': 'Latte', 'quantity': 25, 'revenue': 137.50, 'avg_price': 5.50, 'margin': 77.1, 'last_sale': '2025-08-08'},
                ]
                products_table.setRowCount(len(sample_data))
                for row, product in enumerate(sample_data):
                    products_table.setItem(row, 0, QTableWidgetItem(product['name']))
                    products_table.setItem(row, 1, QTableWidgetItem(str(product['quantity'])))
                    products_table.setItem(row, 2, QTableWidgetItem(f"${product['revenue']:.2f}"))
                    products_table.setItem(row, 3, QTableWidgetItem(f"${product['avg_price']:.2f}"))
                    products_table.setItem(row, 4, QTableWidgetItem(f"{product['margin']:.1f}%"))
                    products_table.setItem(row, 5, QTableWidgetItem(product['last_sale']))
        except Exception as e:
            print(f"Error cargando productos: {e}")
            products_table.setRowCount(1)
            products_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
        
        products_table.resizeColumnsToContents()
        layout.addWidget(products_table)
        
        return widget

    def create_categories_analysis_tab(self, start_date_widget, end_date_widget):
        """Crear pestaña de análisis de categorías"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tabla de categorías
        categories_table = QTableWidget()
        categories_table.setColumnCount(6)
        categories_table.setHorizontalHeaderLabels([
            "Categoría", "Productos Vendidos", "Ingresos Totales", 
            "Participación (%)", "Crecimiento", "Tendencia"
        ])
        
        # Datos de muestra para categorías
        sample_data = [
            {'name': 'Bebidas Calientes', 'products_sold': 102, 'revenue': 477.50, 'participation': 45.2, 'growth': 12.5, 'trend': '↗️ Creciendo'},
            {'name': 'Panadería', 'products_sold': 72, 'revenue': 198.00, 'participation': 28.3, 'growth': 8.2, 'trend': '↗️ Creciendo'},
            {'name': 'Sándwiches', 'products_sold': 18, 'revenue': 144.00, 'participation': 15.1, 'growth': -2.1, 'trend': '↘️ Declinando'},
            {'name': 'Bebidas Frías', 'products_sold': 15, 'revenue': 45.00, 'participation': 8.8, 'growth': 5.3, 'trend': '➡️ Estable'},
            {'name': 'Snacks', 'products_sold': 8, 'revenue': 32.00, 'participation': 2.6, 'growth': 15.7, 'trend': '↗️ Creciendo'},
        ]
        
        categories_table.setRowCount(len(sample_data))
        for row, category in enumerate(sample_data):
            categories_table.setItem(row, 0, QTableWidgetItem(category['name']))
            categories_table.setItem(row, 1, QTableWidgetItem(str(category['products_sold'])))
            categories_table.setItem(row, 2, QTableWidgetItem(f"${category['revenue']:.2f}"))
            categories_table.setItem(row, 3, QTableWidgetItem(f"{category['participation']:.1f}%"))
            categories_table.setItem(row, 4, QTableWidgetItem(f"{category['growth']:.1f}%"))
            categories_table.setItem(row, 5, QTableWidgetItem(category['trend']))
        
        categories_table.resizeColumnsToContents()
        layout.addWidget(categories_table)
        
        return widget

    def create_hours_analysis_tab(self, start_date_widget, end_date_widget):
        """Crear pestaña de análisis horario"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tabla de horas
        hours_table = QTableWidget()
        hours_table.setColumnCount(7)
        hours_table.setHorizontalHeaderLabels([
            "Hora", "Ventas Totales", "Ingresos", "Promedio por Venta", 
            "Órdenes", "Eficiencia", "Tendencia"
        ])
        
        # Datos de muestra para horas
        sample_data = [
            {'hour': '08:00', 'total_sales': 12, 'revenue': 62.50, 'orders': 12, 'efficiency': 'Baja', 'trend': '➡️ Estable'},
            {'hour': '09:00', 'total_sales': 28, 'revenue': 142.00, 'orders': 25, 'efficiency': 'Media', 'trend': '↗️ Creciendo'},
            {'hour': '10:00', 'total_sales': 45, 'revenue': 234.75, 'orders': 42, 'efficiency': 'Alta', 'trend': '↗️ Creciendo'},
            {'hour': '11:00', 'total_sales': 38, 'revenue': 198.50, 'orders': 35, 'efficiency': 'Alta', 'trend': '➡️ Estable'},
            {'hour': '12:00', 'total_sales': 52, 'revenue': 287.00, 'orders': 48, 'efficiency': 'Muy Alta', 'trend': '↗️ Creciendo'},
            {'hour': '13:00', 'total_sales': 44, 'revenue': 245.20, 'orders': 41, 'efficiency': 'Alta', 'trend': '↘️ Declinando'},
            {'hour': '14:00', 'total_sales': 31, 'revenue': 167.75, 'orders': 28, 'efficiency': 'Media', 'trend': '↘️ Declinando'},
            {'hour': '15:00', 'total_sales': 22, 'revenue': 118.50, 'orders': 20, 'efficiency': 'Media', 'trend': '↘️ Declinando'},
            {'hour': '16:00', 'total_sales': 25, 'revenue': 137.25, 'orders': 23, 'efficiency': 'Media', 'trend': '↗️ Creciendo'},
            {'hour': '17:00', 'total_sales': 19, 'revenue': 98.75, 'orders': 17, 'efficiency': 'Baja', 'trend': '➡️ Estable'},
            {'hour': '18:00', 'total_sales': 15, 'revenue': 78.00, 'orders': 14, 'efficiency': 'Baja', 'trend': '↘️ Declinando'},
        ]
        
        hours_table.setRowCount(len(sample_data))
        for row, hour_data in enumerate(sample_data):
            avg_sale = hour_data['revenue'] / hour_data['total_sales'] if hour_data['total_sales'] > 0 else 0
            hours_table.setItem(row, 0, QTableWidgetItem(hour_data['hour']))
            hours_table.setItem(row, 1, QTableWidgetItem(str(hour_data['total_sales'])))
            hours_table.setItem(row, 2, QTableWidgetItem(f"${hour_data['revenue']:.2f}"))
            hours_table.setItem(row, 3, QTableWidgetItem(f"${avg_sale:.2f}"))
            hours_table.setItem(row, 4, QTableWidgetItem(str(hour_data['orders'])))
            hours_table.setItem(row, 5, QTableWidgetItem(hour_data['efficiency']))
            hours_table.setItem(row, 6, QTableWidgetItem(hour_data['trend']))
        
        hours_table.resizeColumnsToContents()
        layout.addWidget(hours_table)
        
        return widget

    def create_header(self):
        """Crear header con título y controles principales"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 5px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                padding: 5px;
                max-height: 100px;
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
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-7))
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
        """Crear panel izquierdo con métricas clave"""
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
        
        # Título del panel
        title = QLabel("📈 Métricas Clave")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            padding-bottom: 10px;
            border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
        """)
        layout.addWidget(title)
        
        # Métricas principales en grid compacto 2x2
        metrics_frame = QFrame()
        metrics_layout = QGridLayout(metrics_frame)
        metrics_layout.setSpacing(8)
        metrics_layout.setContentsMargins(0, 10, 0, 10)
        
        # Crear métricas más compactas
        self.sales_metric = self.create_compact_metric_widget("💰", "Ventas", "$0.00", ColorPalette.SUCCESS)
        self.orders_metric = self.create_compact_metric_widget("📋", "Órdenes", "0", ColorPalette.YINMN_BLUE)
        self.avg_ticket_metric = self.create_compact_metric_widget("🎯", "Promedio", "$0.00", ColorPalette.WARNING)
        self.margin_metric = self.create_compact_metric_widget("📊", "Margen", "0%", ColorPalette.ERROR)
        
        # Distribuir en grid 2x2
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
        
        # Botones de período en grid horizontal para ahorrar espacio
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(4)
        
        # Botones más compactos
        today_btn = QPushButton("📅 Hoy")
        week_btn = QPushButton("📆 Semana")
        month_btn = QPushButton("🗓️ Mes")
        
        # Distribuir en 3 columnas para pantallas pequeñas
        buttons_layout.addWidget(today_btn, 0, 0)
        buttons_layout.addWidget(week_btn, 0, 1)
        buttons_layout.addWidget(month_btn, 0, 2)
        
        # Conectar eventos
        today_btn.clicked.connect(lambda: self.set_quick_period("today"))
        week_btn.clicked.connect(lambda: self.set_quick_period("week"))
        month_btn.clicked.connect(lambda: self.set_quick_period("month"))
        
        # Estilo compacto para botones
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
        
        # Sección de análisis detallado
        analysis_frame = QFrame()
        analysis_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        analysis_layout = QVBoxLayout(analysis_frame)
        analysis_layout.setSpacing(6)
        
        analysis_title = QLabel("🔍 Análisis Detallado")
        analysis_title.setStyleSheet("font-weight: bold; font-size: 12px; margin-bottom: 5px;")
        analysis_layout.addWidget(analysis_title)
        
        # Descripción de lo que incluye
        description_label = QLabel("• Productos más vendidos\n• Análisis por categorías\n• Tendencias horarias")
        description_label.setStyleSheet(f"""
            font-size: 10px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
            padding: 5px;
        """)
        analysis_layout.addWidget(description_label)
        
        layout.addWidget(analysis_frame)
        
        # Botón exportar más compacto
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
        layout.addWidget(export_btn)
        
        # Configurar scroll area
        scroll_area.setWidget(scroll_content)
        
        # Layout principal del panel
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.addWidget(scroll_area)
        
        return panel

    def create_right_panel(self):
        """Crear panel derecho con gráficos expandidos"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 10px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        layout = QVBoxLayout(panel)
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
        
        # Área de gráficos expandida (ocupa todo el espacio disponible)
        charts_frame = QFrame()
        charts_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        charts_layout = QVBoxLayout(charts_frame)
        charts_layout.setContentsMargins(10, 10, 10, 10)
        
        # Gráfico de ventas diarias expandido
        self.sales_chart = self.create_sales_chart()
        charts_layout.addWidget(self.sales_chart)
        
        layout.addWidget(charts_frame)
        
        return panel

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
                min-height: 50px;
                max-height: 65px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)
        
        # Header con icono y título en una línea
        header_layout = QHBoxLayout()
        header_layout.setSpacing(4)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 16px;
            color: {color};
            min-width: 20px;
            max-width: 20px;
        """)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 10px;
            font-weight: bold;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.8)};
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valor
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {color};
            text-align: center;
        """)
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        # Guardar referencia al label de valor para actualizaciones
        widget.value_label = value_label
        
        return widget

    def create_sales_chart(self):
        """Crear gráfico de ventas diarias expandido"""
        # Crear figura de matplotlib más grande para aprovechar el espacio
        self.figure = Figure(figsize=(12, 6), dpi=100)
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
                
                self.sales_metric.value_label.setText(f"${total_sales:.2f}")
                self.orders_metric.value_label.setText(str(total_orders))
                self.avg_ticket_metric.value_label.setText(f"${avg_ticket:.2f}")
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
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
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
                
                ax.plot(dates, sales, marker='o', linewidth=2, markersize=6, color='#2E86AB')
                ax.fill_between(dates, sales, alpha=0.3, color='#2E86AB')
                
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//7)))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
                
                max_sales = max(sales) if sales else 0
                if max_sales > 0:
                    ax.set_ylim(0, max_sales * 1.1)
            else:
                ax.text(0.5, 0.5, 'No hay datos para el período seleccionado\nPrueba con otro rango de fechas', 
                       ha='center', va='center', transform=ax.transAxes,
                       fontsize=12, color='#333333')
            
            ax.set_title('Ventas Diarias', fontsize=12, fontweight='bold', color='#333333', pad=10)
            ax.set_xlabel('Fecha', fontweight='bold', fontsize=10)
            ax.set_ylabel('Ventas ($)', fontweight='bold', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            ax.tick_params(axis='both', which='major', labelsize=9)
            
            self.figure.tight_layout(pad=1.5)
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error cargando gráfico de ventas: {e}")
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f'Error cargando datos:\n{str(e)}', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12, color='red')
            ax.set_title('Error en Gráfico', fontsize=14, fontweight='bold')
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
