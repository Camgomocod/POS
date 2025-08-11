# views/reports_view_pyqtgraph.py
import os
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
from datetime import datetime, timedelta
import csv
import traceback

# Importación de PyQtGraph
PYQTGRAPH_AVAILABLE = True
try:
    import pyqtgraph as pg
    from pyqtgraph import PlotWidget, BarGraphItem
    import numpy as np
    print("✅ PyQtGraph cargado correctamente")
    
    # Configurar PyQtGraph para mejor apariencia
    pg.setConfigOption('background', 'w')  # Fondo blanco
    pg.setConfigOption('foreground', 'k')  # Texto negro
    pg.setConfigOption('antialias', True)  # Antialiasing para mejor calidad
    
except ImportError as e:
    print(f"⚠️  PyQtGraph no disponible: {e}")
    PYQTGRAPH_AVAILABLE = False
    
    # Clases dummy si no está disponible
    class PlotWidget(QWidget):
        def __init__(self, parent=None, **kwargs):
            super().__init__(parent)
            self.setMinimumSize(400, 300)
            self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
            
        def plot(self, *args, **kwargs):
            pass
            
        def clear(self):
            pass
            
        def setLabel(self, *args, **kwargs):
            pass
            
        def addItem(self, *args, **kwargs):
            pass
            
        def getAxis(self, *args, **kwargs):
            return DummyAxis()
            
        def setTitle(self, *args, **kwargs):
            pass
    
    class BarGraphItem:
        def __init__(self, *args, **kwargs):
            pass
    
    class DummyAxis:
        def setTicks(self, *args, **kwargs):
            pass
    
    np = None

class ReportsView(QWidget):
    """Vista principal de reportes con análisis detallado integrado usando PyQtGraph"""
    
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
        self.details_btn.setText("📈 Volver a Gráficos")
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
        self.details_btn.setText("📊 Ver Análisis Detallado")
        
        # Recargar el gráfico
        self.load_sales_chart()
        print("✅ Modo principal activado")

    def clear_right_panel_content(self):
        """Limpiar el contenido del panel derecho"""
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
            self.load_products_data(products_table)
        except Exception as e:
            print(f"Error cargando datos de productos: {e}")
        
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
            self.load_categories_data(categories_table)
        except Exception as e:
            print(f"Error cargando datos de categorías: {e}")
        
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
            self.load_hours_data(hours_table)
        except Exception as e:
            print(f"Error cargando datos de horas: {e}")
        
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
        
        filters_layout.addWidget(QLabel("Desde:"))
        
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
        """Crear frame con gráficos PyQtGraph"""
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
        
        if PYQTGRAPH_AVAILABLE:
            # Crear gráfico principal de ventas con PyQtGraph
            self.sales_chart = self.create_pyqtgraph_sales_chart()
            charts_layout.addWidget(self.sales_chart)
            
            # Agregar gráfico de productos más vendidos
            products_chart = self.create_pyqtgraph_products_chart()
            charts_layout.addWidget(products_chart)
        else:
            # Placeholder si PyQtGraph no está disponible
            placeholder = QLabel("📊 Gráficos interactivos\n(PyQtGraph no disponible)\n\nInstalar: pip install pyqtgraph")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet(f"""
                QLabel {{
                    background-color: {ColorPalette.PLATINUM};
                    border-radius: 8px;
                    min-height: 400px;
                    font-size: 16px;
                    color: #666;
                    border: 2px dashed #ccc;
                }}
            """)
            charts_layout.addWidget(placeholder)
        
        return charts_frame

    def create_pyqtgraph_sales_chart(self):
        """Crear gráfico de ventas con PyQtGraph"""
        # Crear widget del gráfico
        sales_plot = PlotWidget(title="📈 Ventas Diarias")
        sales_plot.setLabel('left', 'Ventas ($)', units='$')
        sales_plot.setLabel('bottom', 'Días')
        sales_plot.showGrid(x=True, y=True, alpha=0.3)
        sales_plot.setMinimumHeight(300)
        
        # Personalizar apariencia
        sales_plot.setStyleSheet(f"""
            PlotWidget {{
                background-color: white;
                border-radius: 8px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
            }}
        """)
        
        # Guardar referencia para poder actualizar después
        self.sales_plot_widget = sales_plot
        
        return sales_plot

    def create_pyqtgraph_products_chart(self):
        """Crear gráfico de productos más vendidos con PyQtGraph"""
        # Crear widget del gráfico
        products_plot = PlotWidget(title="🏆 Top 5 Productos Más Vendidos")
        products_plot.setLabel('left', 'Cantidad')
        products_plot.setLabel('bottom', 'Productos')
        products_plot.showGrid(x=False, y=True, alpha=0.3)
        products_plot.setMinimumHeight(250)
        
        # Personalizar apariencia
        products_plot.setStyleSheet(f"""
            PlotWidget {{
                background-color: white;
                border-radius: 8px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.3)};
            }}
        """)
        
        # Guardar referencia para poder actualizar después
        self.products_plot_widget = products_plot
        
        return products_plot

    def load_sales_chart(self):
        """Cargar datos en el gráfico de ventas PyQtGraph"""
        if not PYQTGRAPH_AVAILABLE:
            return
            
        try:
            # Obtener datos de ventas
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Obtener datos del controlador
            daily_data = self.reports_ctrl.get_daily_sales(start_date, end_date)
            
            if not daily_data:
                # Datos de ejemplo si no hay datos reales
                daily_data = self.get_sample_sales_data()
            
            # Preparar datos para PyQtGraph
            days = []
            sales = []
            
            for i, (date, amount) in enumerate(daily_data):
                days.append(i)
                sales.append(float(amount))
            
            # Limpiar gráfico anterior
            self.sales_plot_widget.clear()
            
            # Crear línea de ventas
            pen = pg.mkPen(color='#1f77b4', width=3)
            brush = pg.mkBrush(color=(31, 119, 180, 100))
            
            # Línea principal
            line = self.sales_plot_widget.plot(days, sales, pen=pen, 
                                             symbol='o', symbolBrush='#1f77b4', 
                                             symbolSize=8, name='Ventas')
            
            # Área bajo la curva para mejor efecto visual
            if len(days) > 1:
                fill_curve = pg.PlotCurveItem(days, sales, pen=pen)
                fill = pg.FillBetweenItem(fill_curve, pg.PlotCurveItem(days, [0]*len(days)), brush=brush)
                self.sales_plot_widget.addItem(fill)
                self.sales_plot_widget.addItem(line)
            
            # Configurar etiquetas del eje X con fechas
            if daily_data:
                date_labels = [(i, data[0].strftime('%m/%d') if hasattr(data[0], 'strftime') else str(data[0])) 
                              for i, data in enumerate(daily_data[::max(1, len(daily_data)//7)])]
                ax = self.sales_plot_widget.getAxis('bottom')
                ax.setTicks([date_labels])
            
            # Actualizar productos chart también
            self.load_products_chart()
            
            print("✅ Gráfico de ventas PyQtGraph cargado")
            
        except Exception as e:
            print(f"❌ Error cargando gráfico de ventas: {e}")
            traceback.print_exc()

    def load_products_chart(self):
        """Cargar datos en el gráfico de productos PyQtGraph"""
        if not PYQTGRAPH_AVAILABLE:
            return
            
        try:
            # Obtener datos de productos más vendidos
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            products_data = self.reports_ctrl.get_top_products(start_date, end_date, limit=5)
            
            if not products_data:
                # Datos de ejemplo si no hay datos reales
                products_data = [
                    ("Producto A", 45),
                    ("Producto B", 38),
                    ("Producto C", 32),
                    ("Producto D", 28),
                    ("Producto E", 25)
                ]
            
            # Preparar datos para gráfico de barras
            x_pos = list(range(len(products_data)))
            quantities = [float(data[1]) for data in products_data]
            product_names = [data[0][:12] + "..." if len(data[0]) > 12 else data[0] for data in products_data]
            
            # Limpiar gráfico anterior
            self.products_plot_widget.clear()
            
            # Crear gráfico de barras
            if quantities:
                # Crear colores para las barras
                colors = ['#2E8B57', '#4682B4', '#DAA520', '#DC143C', '#8A2BE2']
                brushes = [pg.mkBrush(color=colors[i % len(colors)]) for i in range(len(quantities))]
                
                bar_graph = BarGraphItem(x=x_pos, height=quantities, width=0.6, brushes=brushes)
                self.products_plot_widget.addItem(bar_graph)
                
                # Configurar etiquetas del eje X
                ax = self.products_plot_widget.getAxis('bottom')
                ax.setTicks([[(i, name) for i, name in enumerate(product_names)]])
            
            print("✅ Gráfico de productos PyQtGraph cargado")
            
        except Exception as e:
            print(f"❌ Error cargando gráfico de productos: {e}")
            traceback.print_exc()

    def get_sample_sales_data(self):
        """Obtener datos de ejemplo para ventas"""
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        data = []
        
        for i in range(7):
            date = today - timedelta(days=6-i)
            # Simular ventas variando entre 1000 y 2500
            amount = 1000 + (i * 200) + ((i % 3) * 300)
            data.append((date, amount))
        
        return data

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

    def get_date_edit_style(self):
        """Obtener estilo para QDateEdit"""
        return f"""
            QDateEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.5)};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                min-width: 100px;
            }}
            QDateEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
                background-color: white;
            }}
        """

    def set_quick_period(self, period):
        """Configurar período rápido"""
        today = QDate.currentDate()
        
        if period == "today":
            self.start_date.setDate(today)
            self.end_date.setDate(today)
        elif period == "week":
            self.start_date.setDate(today.addDays(-7))
            self.end_date.setDate(today)
        elif period == "month":
            self.start_date.setDate(today.addDays(-30))
            self.end_date.setDate(today)
        
        self.refresh_data()

    def load_initial_data(self):
        """Cargar datos iniciales"""
        self.load_metrics()
        if PYQTGRAPH_AVAILABLE:
            self.load_sales_chart()

    def refresh_data(self):
        """Actualizar todos los datos"""
        self.load_metrics()
        if PYQTGRAPH_AVAILABLE and self.current_mode == "main":
            self.load_sales_chart()

    def load_metrics(self):
        """Cargar métricas principales"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Obtener métricas del controlador
            metrics = self.reports_ctrl.get_period_metrics(start_date, end_date)
            
            # Actualizar widgets de métricas
            self.sales_metric.value_label.setText(f"${metrics.get('total_sales', 0):,.2f}")
            self.orders_metric.value_label.setText(str(metrics.get('total_orders', 0)))
            self.avg_ticket_metric.value_label.setText(f"${metrics.get('avg_ticket', 0):,.2f}")
            self.margin_metric.value_label.setText(f"{metrics.get('margin_percent', 0):.1f}%")
            
        except Exception as e:
            print(f"Error cargando métricas: {e}")
            # Valores por defecto en caso de error
            self.sales_metric.value_label.setText("$0.00")
            self.orders_metric.value_label.setText("0")
            self.avg_ticket_metric.value_label.setText("$0.00")
            self.margin_metric.value_label.setText("0%")

    def load_products_data(self, table):
        """Cargar datos de productos en tabla"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            products_data = self.reports_ctrl.get_detailed_products_report(start_date, end_date)
            
            table.setRowCount(len(products_data))
            
            for row, product in enumerate(products_data):
                table.setItem(row, 0, QTableWidgetItem(str(product.get('name', ''))))
                table.setItem(row, 1, QTableWidgetItem(str(product.get('quantity', 0))))
                table.setItem(row, 2, QTableWidgetItem(f"${product.get('revenue', 0):,.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"${product.get('avg_price', 0):,.2f}"))
                table.setItem(row, 4, QTableWidgetItem(f"{product.get('margin', 0):.1f}%"))
                table.setItem(row, 5, QTableWidgetItem(str(product.get('last_sale', 'N/A'))))
                
        except Exception as e:
            print(f"Error cargando datos de productos: {e}")

    def load_categories_data(self, table):
        """Cargar datos de categorías en tabla"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            categories_data = self.reports_ctrl.get_categories_report(start_date, end_date)
            
            table.setRowCount(len(categories_data))
            
            for row, category in enumerate(categories_data):
                table.setItem(row, 0, QTableWidgetItem(str(category.get('name', ''))))
                table.setItem(row, 1, QTableWidgetItem(str(category.get('products_sold', 0))))
                table.setItem(row, 2, QTableWidgetItem(f"${category.get('revenue', 0):,.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"${category.get('avg_per_product', 0):,.2f}"))
                table.setItem(row, 4, QTableWidgetItem(f"{category.get('percent_total', 0):.1f}%"))
                
        except Exception as e:
            print(f"Error cargando datos de categorías: {e}")

    def load_hours_data(self, table):
        """Cargar datos horarios en tabla"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            hours_data = self.reports_ctrl.get_hourly_report(start_date, end_date)
            
            table.setRowCount(len(hours_data))
            
            for row, hour_data in enumerate(hours_data):
                table.setItem(row, 0, QTableWidgetItem(str(hour_data.get('hour_range', ''))))
                table.setItem(row, 1, QTableWidgetItem(str(hour_data.get('orders', 0))))
                table.setItem(row, 2, QTableWidgetItem(f"${hour_data.get('revenue', 0):,.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"${hour_data.get('avg_ticket', 0):,.2f}"))
                table.setItem(row, 4, QTableWidgetItem(f"{hour_data.get('percent_total', 0):.1f}%"))
                
        except Exception as e:
            print(f"Error cargando datos horarios: {e}")

    def export_data(self):
        """Exportar datos a CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Reportes", 
                f"reporte_ventas_{datetime.now().strftime('%Y%m%d')}.csv",
                "CSV Files (*.csv)"
            )
            
            if file_path:
                start_date = self.start_date.date().toPyDate()
                end_date = self.end_date.date().toPyDate()
                
                # Exportar datos usando el controlador
                success = self.reports_ctrl.export_reports_to_csv(start_date, end_date, file_path)
                
                if success:
                    QMessageBox.information(self, "Éxito", f"Datos exportados a:\n{file_path}")
                else:
                    QMessageBox.warning(self, "Error", "Error al exportar datos")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en exportación: {str(e)}")
