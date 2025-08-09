# views/reports_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QGridLayout, QDateEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QMessageBox, QFileDialog, QSplitter, QScrollArea)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
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

class ReportsView(QWidget):
    """Vista principal de reportes con métricas esenciales para decisiones de negocio"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_ctrl = MenuController()
        self.order_ctrl = OrderController()
        self.reports_ctrl = ReportsController()
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
        
        # Panel derecho: Gráficos y tablas
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Configurar proporción del splitter adaptativo
        # Para pantallas pequeñas, dar menos espacio al panel izquierdo
        if hasattr(self, 'parent') and self.parent():
            parent_width = self.parent().width() if self.parent().width() > 0 else 1366
        else:
            parent_width = 1366  # Default para pantallas pequeñas
            
        if parent_width <= 1366:
            # Pantalla pequeña: panel izquierdo más estrecho
            splitter.setStretchFactor(0, 1)  # Panel izquierdo
            splitter.setStretchFactor(1, 3)  # Panel derecho (más grande)
            splitter.setSizes([280, 840])  # Tamaños iniciales para pantalla pequeña
        else:
            # Pantalla grande: distribución más balanceada
            splitter.setStretchFactor(0, 1)  # Panel izquierdo
            splitter.setStretchFactor(1, 2)  # Panel derecho
            splitter.setSizes([400, 800])  # Tamaños iniciales para pantalla grande
            
        layout.addWidget(splitter)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
        """)

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
        """Crear panel izquierdo con métricas clave optimizado para pantallas pequeñas"""
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
        
        # Botón exportar más compacto
        export_btn = QPushButton("📤 Exportar")
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
        """Crear panel derecho con gráficos y tablas"""
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
        
        # Área de gráficos con altura fija optimizada
        charts_frame = QFrame()
        charts_frame.setMinimumHeight(300)
        charts_frame.setMaximumHeight(400)  # Limitar altura para dejar espacio a tablas
        charts_layout = QVBoxLayout(charts_frame)
        charts_layout.setContentsMargins(5, 5, 5, 5)
        
        # Gráfico de ventas diarias
        self.sales_chart = self.create_sales_chart()
        charts_layout.addWidget(self.sales_chart)
        
        layout.addWidget(charts_frame)
        
        # Área de tablas con pestañas simuladas
        tables_frame = QFrame()
        tables_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        tables_layout = QVBoxLayout(tables_frame)
        
        # Botones de navegación entre tablas - Optimizado para pantallas pequeñas
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(3)
        
        self.products_tab_btn = QPushButton("🍽️ Productos")
        self.categories_tab_btn = QPushButton("📁 Categorías")
        self.hours_tab_btn = QPushButton("⏰ Horas")
        
        nav_buttons = [self.products_tab_btn, self.categories_tab_btn, self.hours_tab_btn]
        
        for btn in nav_buttons:
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.PLATINUM};
                    color: {ColorPalette.RICH_BLACK};
                    border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                    padding: 6px 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 11px;
                    min-width: 75px;
                    max-height: 30px;
                }}
                QPushButton:checked {{
                    background-color: {ColorPalette.YINMN_BLUE};
                    color: {ColorPalette.PLATINUM};
                }}
                QPushButton:hover {{
                    border-color: {ColorPalette.YINMN_BLUE};
                }}
            """)
            nav_layout.addWidget(btn)
        
        # Conectar eventos
        self.products_tab_btn.clicked.connect(lambda: self.show_table("products"))
        self.categories_tab_btn.clicked.connect(lambda: self.show_table("categories"))
        self.hours_tab_btn.clicked.connect(lambda: self.show_table("hours"))
        
        nav_layout.addStretch()
        tables_layout.addLayout(nav_layout)
        
        # Tabla de datos
        self.data_table = QTableWidget()
        self.setup_table()
        tables_layout.addWidget(self.data_table)
        
        layout.addWidget(tables_frame)
        
        # Seleccionar primera pestaña por defecto
        self.products_tab_btn.setChecked(True)
        self.current_table = "products"
        
        return panel

    def create_metric_widget(self, icon, title, value, color):
        """Crear widget de métrica individual"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(color, 0.1)};
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 10px;
                min-height: 60px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            color: {color};
            min-width: 40px;
        """)
        layout.addWidget(icon_label)
        
        # Contenido
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
        """)
        content_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {color};
        """)
        content_layout.addWidget(value_label)
        
        layout.addLayout(content_layout)
        layout.addStretch()
        
        # Guardar referencia al label de valor para actualizaciones
        widget.value_label = value_label
        
        return widget

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
        """Crear gráfico de ventas diarias"""
        # Crear figura de matplotlib
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # Aplicar estilo
        self.canvas.setStyleSheet(f"""
            FigureCanvas {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 8px;
            }}
        """)
        
        return self.canvas

    def setup_table(self):
        """Configurar tabla de datos - optimizada para pantallas pequeñas"""
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.data_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.data_table.setSortingEnabled(True)
        self.data_table.verticalHeader().setVisible(False)
        
        # Configurar altura de filas más compacta
        self.data_table.horizontalHeader().setDefaultSectionSize(100)
        self.data_table.verticalHeader().setDefaultSectionSize(28)
        
        # Estilo de tabla optimizado para pantallas pequeñas
        self.data_table.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 4px;
                background-color: {ColorPalette.PLATINUM};
                gridline-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                selection-background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
                font-size: 11px;
                min-height: 250px;
                max-height: 350px;
            }}
            QHeaderView::section {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                padding: 6px;
                font-weight: bold;
                font-size: 11px;
                border: none;
                border-right: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.7)};
                max-height: 30px;
            }}
        """)

    def get_date_edit_style(self):
        """Obtener estilo para QDateEdit - optimizado para pantallas pequeñas"""
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
        
        print(f"🗓️ Estableciendo período rápido: {period}")
        
        if period == "today":
            self.start_date.setDate(today)
            self.end_date.setDate(today)
            print(f"📅 Período HOY: {today.toString()}")
        elif period == "week":
            # Lunes de esta semana
            days_since_monday = today.dayOfWeek() - 1
            monday = today.addDays(-days_since_monday)
            self.start_date.setDate(monday)
            self.end_date.setDate(today)
            print(f"📅 Período SEMANA: {monday.toString()} a {today.toString()}")
        elif period == "month":
            # Primer día del mes
            first_day = QDate(today.year(), today.month(), 1)
            self.start_date.setDate(first_day)
            self.end_date.setDate(today)
            print(f"📅 Período MES: {first_day.toString()} a {today.toString()}")
        
        # Forzar actualización de datos
        self.refresh_data()

    def show_table(self, table_type):
        """Mostrar tabla específica"""
        # Desmarcar todos los botones
        self.products_tab_btn.setChecked(False)
        self.categories_tab_btn.setChecked(False)
        self.hours_tab_btn.setChecked(False)
        
        # Marcar el botón seleccionado
        if table_type == "products":
            self.products_tab_btn.setChecked(True)
        elif table_type == "categories":
            self.categories_tab_btn.setChecked(True)
        elif table_type == "hours":
            self.hours_tab_btn.setChecked(True)
        
        self.current_table = table_type
        self.load_table_data()

    def load_initial_data(self):
        """Cargar datos iniciales"""
        self.refresh_data()

    def refresh_data(self):
        """Actualizar todos los datos"""
        try:
            print("🔄 Iniciando actualización de datos de reportes...")
            
            # Cargar métricas primero
            print("📊 1. Cargando métricas...")
            self.load_metrics()
            
            # Luego cargar gráfico
            print("📈 2. Cargando gráfico de ventas...")
            self.load_sales_chart()
            
            # Finalmente cargar tabla
            print("📋 3. Cargando datos de tabla...")
            self.load_table_data()
            
            print("✅ Actualización de datos completada")
            
        except Exception as e:
            print(f"❌ Error general en refresh_data: {e}")
            import traceback
            traceback.print_exc()

    def load_metrics(self):
        """Cargar métricas principales"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            print(f"📊 Cargando métricas del {start_date} al {end_date}")
            
            # Obtener datos reales usando el controlador de reportes
            sales_summary = self.reports_ctrl.get_sales_summary(start_date, end_date)
            print(f"📊 Resumen de ventas: {sales_summary}")
            
            # Validar que sales_summary contenga los datos esperados
            if sales_summary and isinstance(sales_summary, dict):
                # Calcular métricas con valores por defecto
                total_sales = sales_summary.get('total_sales', 0.0)
                total_orders = sales_summary.get('total_orders', 0)
                avg_ticket = sales_summary.get('avg_ticket', 0.0)
                
                # Obtener análisis de margen
                try:
                    margin_data = self.reports_ctrl.get_profit_margin_analysis(start_date, end_date)
                    overall_margin = margin_data.get('overall_margin', 0.0) if margin_data else 0.0
                except Exception as margin_error:
                    print(f"⚠️ Error obteniendo margen: {margin_error}")
                    overall_margin = 0.0
                
                # Actualizar widgets
                self.sales_metric.value_label.setText(f"${total_sales:.2f}")
                self.orders_metric.value_label.setText(str(total_orders))
                self.avg_ticket_metric.value_label.setText(f"${avg_ticket:.2f}")
                self.margin_metric.value_label.setText(f"{overall_margin:.1f}%")
                
                print(f"✅ Métricas actualizadas: Ventas=${total_sales:.2f}, Órdenes={total_orders}, Promedio=${avg_ticket:.2f}, Margen={overall_margin:.1f}%")
            else:
                print("⚠️ No se obtuvieron datos válidos del resumen de ventas")
                # Valores por defecto si no hay datos
                self.sales_metric.value_label.setText("$0.00")
                self.orders_metric.value_label.setText("0")
                self.avg_ticket_metric.value_label.setText("$0.00")
                self.margin_metric.value_label.setText("0.0%")
            
        except Exception as e:
            print(f"❌ Error cargando métricas: {e}")
            import traceback
            traceback.print_exc()
            
            # Valores por defecto en caso de error
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
            
            print(f"📊 Cargando gráfico de ventas del {start_date} al {end_date}")
            
            # Obtener datos reales de ventas diarias
            daily_sales = self.reports_ctrl.get_daily_sales(start_date, end_date)
            print(f"📊 Datos obtenidos: {daily_sales}")
            
            if daily_sales and len(daily_sales) > 0:
                # Preparar datos para el gráfico
                dates = []
                sales = []
                
                for item in daily_sales:
                    # Convertir fecha string a objeto datetime si es necesario
                    if isinstance(item['date'], str):
                        date_obj = datetime.strptime(item['date'], '%Y-%m-%d').date()
                    else:
                        date_obj = item['date']
                    
                    dates.append(date_obj)
                    sales.append(float(item['total_sales']))
                
                # Crear gráfico con datos reales
                ax.plot(dates, sales, marker='o', linewidth=2, markersize=6, color='#2E86AB')
                ax.fill_between(dates, sales, alpha=0.3, color='#2E86AB')
                
                # Formatear fechas en el eje X
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//7)))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
                
                # Configurar valores en Y
                max_sales = max(sales) if sales else 0
                if max_sales > 0:
                    ax.set_ylim(0, max_sales * 1.1)
            else:
                # Si no hay datos, mostrar mensaje
                ax.text(0.5, 0.5, 'No hay datos para el período seleccionado\nPrueba con otro rango de fechas', 
                       ha='center', va='center', transform=ax.transAxes,
                       fontsize=12, color='#333333')
            
            # Configurar gráfico - optimizado para pantallas pequeñas
            ax.set_title('Ventas Diarias', fontsize=12, fontweight='bold', color='#333333', pad=10)
            ax.set_xlabel('Fecha', fontweight='bold', fontsize=10)
            ax.set_ylabel('Ventas ($)', fontweight='bold', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Configurar tamaño de fuente de los ticks para pantallas pequeñas
            ax.tick_params(axis='both', which='major', labelsize=9)
            
            # Ajustar layout con márgenes más compactos
            self.figure.tight_layout(pad=1.5)
            self.canvas.draw()
            
        except Exception as e:
            print(f"❌ Error cargando gráfico de ventas: {e}")
            import traceback
            traceback.print_exc()
            
            # Mostrar mensaje de error en el gráfico
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f'Error cargando datos:\n{str(e)}', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12, color='red')
            ax.set_title('Error en Gráfico', fontsize=14, fontweight='bold')
            self.canvas.draw()

    def load_table_data(self):
        """Cargar datos de tabla según el tipo seleccionado"""
        try:
            if self.current_table == "products":
                self.load_top_products_table()
            elif self.current_table == "categories":
                self.load_categories_table()
            elif self.current_table == "hours":
                self.load_hours_table()
        except Exception as e:
            print(f"Error cargando tabla: {e}")

    def load_top_products_table(self):
        """Cargar tabla de productos más vendidos"""
        try:
            # Configurar columnas
            columns = ["Producto", "Cantidad Vendida", "Ingresos", "Precio Promedio"]
            self.data_table.setColumnCount(len(columns))
            self.data_table.setHorizontalHeaderLabels(columns)
            
            # Obtener datos reales
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            products_data = self.reports_ctrl.get_top_products(start_date, end_date, limit=10)
            
            if products_data and len(products_data) > 0:
                self.data_table.setRowCount(len(products_data))
                
                for row, product in enumerate(products_data):
                    self.data_table.setItem(row, 0, QTableWidgetItem(str(product.get('name', 'Sin nombre'))))
                    self.data_table.setItem(row, 1, QTableWidgetItem(str(product.get('quantity', 0))))
                    self.data_table.setItem(row, 2, QTableWidgetItem(f"${product.get('revenue', 0):.2f}"))
                    self.data_table.setItem(row, 3, QTableWidgetItem(f"${product.get('avg_price', 0):.2f}"))
            else:
                # Mostrar una fila indicando que no hay datos
                self.data_table.setRowCount(1)
                self.data_table.setItem(0, 0, QTableWidgetItem("No hay datos disponibles"))
                for i in range(1, len(columns)):
                    self.data_table.setItem(0, i, QTableWidgetItem("-"))
            
            # Ajustar columnas
            header = self.data_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            for i in range(1, len(columns)):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                
        except Exception as e:
            print(f"❌ Error cargando tabla de productos: {e}")
            import traceback
            traceback.print_exc()
            # Mostrar tabla con mensaje de error
            self.data_table.setRowCount(1)
            self.data_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
            for i in range(1, 4):
                self.data_table.setItem(0, i, QTableWidgetItem("-"))

    def load_categories_table(self):
        """Cargar tabla de ventas por categorías"""
        try:
            columns = ["Categoría", "Órdenes", "Ingresos", "% del Total", "Items Vendidos"]
            self.data_table.setColumnCount(len(columns))
            self.data_table.setHorizontalHeaderLabels(columns)
            
            # Obtener datos reales
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            categories_data = self.reports_ctrl.get_sales_by_category(start_date, end_date)
            
            if categories_data and len(categories_data) > 0:
                self.data_table.setRowCount(len(categories_data))
                
                for row, category in enumerate(categories_data):
                    self.data_table.setItem(row, 0, QTableWidgetItem(str(category.get('name', 'Sin nombre'))))
                    self.data_table.setItem(row, 1, QTableWidgetItem(str(category.get('order_count', 0))))
                    self.data_table.setItem(row, 2, QTableWidgetItem(f"${category.get('revenue', 0):.2f}"))
                    self.data_table.setItem(row, 3, QTableWidgetItem(f"{category.get('percentage', 0):.1f}%"))
                    self.data_table.setItem(row, 4, QTableWidgetItem(str(category.get('total_items', 0))))
            else:
                # Mostrar una fila indicando que no hay datos
                self.data_table.setRowCount(1)
                self.data_table.setItem(0, 0, QTableWidgetItem("No hay datos disponibles"))
                for i in range(1, len(columns)):
                    self.data_table.setItem(0, i, QTableWidgetItem("-"))
            
            # Ajustar columnas
            header = self.data_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            for i in range(1, len(columns)):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                
        except Exception as e:
            print(f"❌ Error cargando tabla de categorías: {e}")
            import traceback
            traceback.print_exc()
            # Mostrar tabla con mensaje de error
            self.data_table.setRowCount(1)
            self.data_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
            for i in range(1, 5):
                self.data_table.setItem(0, i, QTableWidgetItem("-"))

    def load_hours_table(self):
        """Cargar tabla de análisis por horas"""
        try:
            columns = ["Hora", "Órdenes", "Ingresos", "Ticket Promedio", "% del Día"]
            self.data_table.setColumnCount(len(columns))
            self.data_table.setHorizontalHeaderLabels(columns)
            
            # Obtener datos reales
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            hours_data = self.reports_ctrl.get_sales_by_hour(start_date, end_date)
            
            if hours_data and len(hours_data) > 0:
                self.data_table.setRowCount(len(hours_data))
                
                for row, hour_data in enumerate(hours_data):
                    self.data_table.setItem(row, 0, QTableWidgetItem(str(hour_data.get('hour_range', 'N/A'))))
                    self.data_table.setItem(row, 1, QTableWidgetItem(str(hour_data.get('order_count', 0))))
                    self.data_table.setItem(row, 2, QTableWidgetItem(f"${hour_data.get('total_sales', 0):.2f}"))
                    self.data_table.setItem(row, 3, QTableWidgetItem(f"${hour_data.get('avg_ticket', 0):.2f}"))
                    self.data_table.setItem(row, 4, QTableWidgetItem(f"{hour_data.get('percentage', 0):.1f}%"))
            else:
                # Mostrar una fila indicando que no hay datos
                self.data_table.setRowCount(1)
                self.data_table.setItem(0, 0, QTableWidgetItem("No hay datos disponibles"))
                for i in range(1, len(columns)):
                    self.data_table.setItem(0, i, QTableWidgetItem("-"))
            
            # Ajustar columnas
            header = self.data_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            for i in range(1, len(columns)):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                
        except Exception as e:
            print(f"❌ Error cargando tabla de horas: {e}")
            import traceback
            traceback.print_exc()
            # Mostrar tabla con mensaje de error
            self.data_table.setRowCount(1)
            self.data_table.setItem(0, 0, QTableWidgetItem(f"Error: {str(e)}"))
            for i in range(1, 5):
                self.data_table.setItem(0, i, QTableWidgetItem("-"))

    def get_orders_data(self, start_date, end_date):
        """Obtener datos de órdenes (simulado - implementar con controlador real)"""
        # Esta función debería obtener datos reales de la base de datos
        # Por ahora retorna datos simulados
        orders = []
        current_date = start_date
        
        while current_date <= end_date:
            # Simular 10-30 órdenes por día
            daily_orders = 15 + (current_date.weekday() * 2)
            
            for i in range(daily_orders):
                orders.append({
                    'date': current_date,
                    'total': 8.00 + (i % 20),  # Simular precios variables
                    'items_count': 1 + (i % 4)
                })
            
            current_date += timedelta(days=1)
        
        return orders

    def export_data(self):
        """Exportar datos a CSV"""
        try:
            # Diálogo para seleccionar archivo
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Reportes",
                f"reportes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV files (*.csv)"
            )
            
            if file_path:
                # Exportar datos de la tabla actual
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Headers
                    headers = []
                    for col in range(self.data_table.columnCount()):
                        headers.append(self.data_table.horizontalHeaderItem(col).text())
                    writer.writerow(headers)
                    
                    # Datos
                    for row in range(self.data_table.rowCount()):
                        row_data = []
                        for col in range(self.data_table.columnCount()):
                            item = self.data_table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                    
                    # Información adicional
                    writer.writerow([])
                    writer.writerow(["Información del Reporte"])
                    writer.writerow(["Período:", f"{self.start_date.date().toString()} - {self.end_date.date().toString()}"])
                    writer.writerow(["Generado:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                
                QMessageBox.information(self, "Exportación Exitosa", f"Datos exportados a:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar datos:\n{str(e)}")
