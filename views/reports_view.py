# views/reports_view.py
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

class ReportsView(QWidget):
    switch_to_main = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        print("🔄 Inicializando ReportsView...")
        
        # Inicializar controladores
        self.menu_ctrl = MenuController()
        self.order_ctrl = OrderController()
        self.reports_ctrl = ReportsController()
        
        # Variables de estado
        self.current_mode = "main"
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        
        self.init_ui()
        
        # Cargar datos iniciales
        self.refresh_data()
        
        print("✅ ReportsView inicializado correctamente")

    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        print("🎨 Configurando interfaz de reportes...")
        
        # Layout principal - reducir márgenes para pantallas pequeñas
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Crear splitter para dividir la pantalla
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel izquierdo - Controles y métricas (más compacto)
        left_panel = self.create_left_panel()
        left_panel.setMaximumWidth(320)
        left_panel.setMinimumWidth(280)
        splitter.addWidget(left_panel)
        
        # Panel derecho - Contenido principal
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Configurar proporciones del splitter
        splitter.setStretchFactor(0, 0)  # Panel izquierdo no se estira
        splitter.setStretchFactor(1, 1)  # Panel derecho se estira
        
        print("✅ Interfaz configurada")

    def create_left_panel(self):
        """Crear el panel izquierdo con controles"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Título más compacto
        title_label = QLabel("📊 Reportes")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 5px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Métricas principales (sin controles de fecha)
        metrics_frame = self.create_metrics_frame()
        layout.addWidget(metrics_frame)
        
        # Botones de acción
        buttons_frame = self.create_action_buttons()
        layout.addWidget(buttons_frame)
        
        # Espaciador
        layout.addStretch()
        
        return panel

    def create_metrics_frame(self):
        """Crear el frame de métricas principales"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(6)
        
        # Título más compacto
        title = QLabel("📈 Métricas")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 5px;")
        layout.addWidget(title)
        
        # Grid de métricas más compacto
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(5)
        metrics_grid.setVerticalSpacing(3)
        
        # Total de ventas
        self.sales_label = QLabel("Ventas:")
        self.sales_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 9px;")
        self.sales_value = QLabel("$0")
        self.sales_value.setStyleSheet(f"color: {ColorPalette.SUCCESS}; font-size: 12px; font-weight: bold;")
        self.sales_value.setWordWrap(True)
        
        metrics_grid.addWidget(self.sales_label, 0, 0)
        metrics_grid.addWidget(self.sales_value, 0, 1)
        
        # Número de órdenes
        self.orders_label = QLabel("Órdenes:")
        self.orders_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 9px;")
        self.orders_value = QLabel("0")
        self.orders_value.setStyleSheet(f"color: {ColorPalette.YINMN_BLUE}; font-size: 12px; font-weight: bold;")
        
        metrics_grid.addWidget(self.orders_label, 1, 0)
        metrics_grid.addWidget(self.orders_value, 1, 1)
        
        # Ticket promedio
        self.avg_label = QLabel("Promedio:")
        self.avg_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 9px;")
        self.avg_value = QLabel("$0")
        self.avg_value.setStyleSheet(f"color: {ColorPalette.INFO}; font-size: 12px; font-weight: bold;")
        self.avg_value.setWordWrap(True)
        
        metrics_grid.addWidget(self.avg_label, 2, 0)
        metrics_grid.addWidget(self.avg_value, 2, 1)
        
        # Margen de ganancia
        self.margin_label = QLabel("Margen:")
        self.margin_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 9px;")
        self.margin_value = QLabel("0%")
        self.margin_value.setStyleSheet(f"color: {ColorPalette.WARNING}; font-size: 12px; font-weight: bold;")
        
        metrics_grid.addWidget(self.margin_label, 3, 0)
        metrics_grid.addWidget(self.margin_value, 3, 1)
        
        # Configurar el ancho de las columnas
        metrics_grid.setColumnStretch(0, 0)  # Columna de etiquetas no se estira
        metrics_grid.setColumnStretch(1, 1)  # Columna de valores se estira
        
        layout.addLayout(metrics_grid)
        
        return frame

    def create_action_buttons(self):
        """Crear botones de acción"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(6)
        
        # Botón de análisis detallado
        self.details_btn = QPushButton("📋 Detallado")
        self.details_btn.clicked.connect(self.toggle_detailed_view)
        self.details_btn.setStyleSheet(self.get_primary_button_style())
        self.details_btn.setMaximumHeight(30)
        layout.addWidget(self.details_btn)
        
        # Botón de exportar
        export_btn = QPushButton("📤 Exportar")
        export_btn.clicked.connect(self.export_report)
        export_btn.setStyleSheet(self.get_secondary_button_style())
        export_btn.setMaximumHeight(30)
        layout.addWidget(export_btn)
        
        # Botón de actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setStyleSheet(self.get_secondary_button_style())
        refresh_btn.setMaximumHeight(30)
        layout.addWidget(refresh_btn)
        
        return frame

    def create_right_panel(self):
        """Crear el panel derecho"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
            }}
        """)
        
        # Layout principal del panel derecho - más compacto
        self.right_layout = QVBoxLayout(panel)
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.right_layout.setSpacing(8)
        
        # Layout para el contenido que cambia
        self.right_content_layout = QVBoxLayout()
        self.right_layout.addLayout(self.right_content_layout)
        
        # Mostrar vista principal por defecto
        self.show_main_view()
        
        return panel

    def show_main_view(self):
        """Mostrar la vista principal con resumen financiero y tablas"""
        self.clear_right_panel_content()
        self.current_mode = "main"
        
        # Título más compacto
        title = QLabel("📊 Resumen Financiero")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        self.right_content_layout.addWidget(title)
        
        # Crear contenido principal con tabs
        self.create_main_financial_summary()
        
        # Actualizar el botón
        self.details_btn.setText("📋 Estadísticas")
        
        print("✅ Modo principal activado")

    def create_main_financial_summary(self):
        """Crear el resumen financiero principal"""
        # Añadir controles de fecha al inicio del panel derecho
        date_controls_frame = self.create_main_date_controls()
        self.right_content_layout.addWidget(date_controls_frame)
        
        # Crear tabs para el resumen principal
        main_tab_widget = QTabWidget()
        main_tab_widget.setStyleSheet(self.get_tab_style())
        
        # Tab de resumen por período
        summary_tab = self.create_period_summary_tab()
        main_tab_widget.addTab(summary_tab, "📅 Por Período")
        
        # Tab de productos top
        products_tab = self.create_top_products_tab()
        main_tab_widget.addTab(products_tab, "🏆 Top Productos")
        
        # Tab de análisis mensual
        monthly_tab = self.create_monthly_analysis_tab()
        main_tab_widget.addTab(monthly_tab, "📊 Análisis Mensual")
        
        self.right_content_layout.addWidget(main_tab_widget)

    def create_main_date_controls(self):
        """Crear controles de fecha para el panel principal"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 10px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("📅 Seleccionar Período:")
        title.setFont(QFont("Arial", 11, QFont.Bold))
        title.setStyleSheet(f"color: {ColorPalette.RICH_BLACK};")
        layout.addWidget(title)
        
        # Fecha inicio
        start_label = QLabel("Desde:")
        start_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 10px;")
        layout.addWidget(start_label)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.start_date.setStyleSheet(self.get_date_edit_style())
        self.start_date.setMinimumHeight(28)
        self.start_date.setMaximumHeight(28)
        self.start_date.setMinimumWidth(100)
        self.start_date.dateChanged.connect(self.refresh_data)
        layout.addWidget(self.start_date)
        
        # Fecha fin
        end_label = QLabel("Hasta:")
        end_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 10px;")
        layout.addWidget(end_label)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setStyleSheet(self.get_date_edit_style())
        self.end_date.setMinimumHeight(28)
        self.end_date.setMaximumHeight(28)
        self.end_date.setMinimumWidth(100)
        self.end_date.dateChanged.connect(self.refresh_data)
        layout.addWidget(self.end_date)
        
        # Separador
        separator = QLabel("|")
        separator.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE}; font-size: 14px;")
        layout.addWidget(separator)
        
        # Botones de períodos rápidos
        today_btn = QPushButton("Hoy")
        today_btn.clicked.connect(lambda: self.set_date_range(0))
        today_btn.setStyleSheet(self.get_small_button_style())
        today_btn.setMaximumHeight(26)
        layout.addWidget(today_btn)
        
        week_btn = QPushButton("7 días")
        week_btn.clicked.connect(lambda: self.set_date_range(7))
        week_btn.setStyleSheet(self.get_small_button_style())
        week_btn.setMaximumHeight(26)
        layout.addWidget(week_btn)
        
        month_btn = QPushButton("30 días")
        month_btn.clicked.connect(lambda: self.set_date_range(30))
        month_btn.setStyleSheet(self.get_small_button_style())
        month_btn.setMaximumHeight(26)
        layout.addWidget(month_btn)
        
        # Espaciador
        layout.addStretch()
        
        return frame

    def create_period_summary_tab(self):
        """Crear tab de resumen por período"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        
        # Controles de período
        period_controls = QHBoxLayout()
        period_controls.setSpacing(5)
        
        period_label = QLabel("Ver por:")
        period_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 10px;")
        period_controls.addWidget(period_label)
        
        # Botones de período
        self.day_btn = QPushButton("Día")
        self.day_btn.clicked.connect(lambda: self.change_period_view("day"))
        self.day_btn.setStyleSheet(self.get_period_button_style(True))
        self.day_btn.setMaximumHeight(25)
        
        self.week_btn = QPushButton("Semana")
        self.week_btn.clicked.connect(lambda: self.change_period_view("week"))
        self.week_btn.setStyleSheet(self.get_period_button_style(False))
        self.week_btn.setMaximumHeight(25)
        
        self.month_btn = QPushButton("Mes")
        self.month_btn.clicked.connect(lambda: self.change_period_view("month"))
        self.month_btn.setStyleSheet(self.get_period_button_style(False))
        self.month_btn.setMaximumHeight(25)
        
        period_controls.addWidget(self.day_btn)
        period_controls.addWidget(self.week_btn)
        period_controls.addWidget(self.month_btn)
        period_controls.addStretch()
        
        layout.addLayout(period_controls)
        
        # Tabla de resumen por período
        self.period_summary_table = QTableWidget()
        self.period_summary_table.setStyleSheet(self.get_table_style())
        self.period_summary_table.verticalHeader().setVisible(False)
        
        # Variable para controlar el período actual
        self.current_period = "day"
        
        # Cargar datos iniciales
        self.load_period_summary_data()
        
        layout.addWidget(self.period_summary_table)
        
        return widget

    def create_top_products_tab(self):
        """Crear tab de productos más vendidos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        
        # Tabla de productos top
        self.top_products_table = QTableWidget()
        self.top_products_table.setStyleSheet(self.get_table_style())
        self.top_products_table.setColumnCount(4)
        self.top_products_table.setHorizontalHeaderLabels([
            "Producto", "Vendidos", "Ingresos", "% Total"
        ])
        self.top_products_table.verticalHeader().setVisible(False)
        
        # Configurar anchos
        self.top_products_table.setColumnWidth(0, 120)
        self.top_products_table.setColumnWidth(1, 60)
        self.top_products_table.setColumnWidth(2, 80)
        self.top_products_table.setColumnWidth(3, 50)
        
        header = self.top_products_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.top_products_table.setAlternatingRowColors(True)
        
        # Cargar datos
        self.load_top_products_data()
        
        layout.addWidget(self.top_products_table)
        
        return widget

    def create_monthly_analysis_tab(self):
        """Crear tab de análisis mensual"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        
        # Resumen del mes actual
        current_month_frame = QFrame()
        current_month_frame.setFrameStyle(QFrame.StyledPanel)
        current_month_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 10px;
            }}
        """)
        
        month_layout = QVBoxLayout(current_month_frame)
        month_layout.setSpacing(5)
        
        # Título del mes
        from datetime import datetime
        current_month_name = datetime.now().strftime("%B %Y")
        month_title = QLabel(f"📅 {current_month_name}")
        month_title.setFont(QFont("Arial", 12, QFont.Bold))
        month_title.setStyleSheet(f"color: {ColorPalette.RICH_BLACK};")
        month_layout.addWidget(month_title)
        
        # Grid de métricas mensuales
        self.monthly_metrics_layout = QGridLayout()
        self.monthly_metrics_layout.setSpacing(5)
        month_layout.addLayout(self.monthly_metrics_layout)
        
        layout.addWidget(current_month_frame)
        
        # Tabla de comparación mensual
        monthly_comparison_label = QLabel("📊 Comparación Mensual")
        monthly_comparison_label.setFont(QFont("Arial", 11, QFont.Bold))
        monthly_comparison_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK};")
        layout.addWidget(monthly_comparison_label)
        
        self.monthly_table = QTableWidget()
        self.monthly_table.setStyleSheet(self.get_table_style())
        self.monthly_table.setColumnCount(4)
        self.monthly_table.setHorizontalHeaderLabels([
            "Mes", "Ventas", "Órdenes", "Promedio"
        ])
        self.monthly_table.verticalHeader().setVisible(False)
        
        # Configurar anchos
        self.monthly_table.setColumnWidth(0, 80)
        self.monthly_table.setColumnWidth(1, 80)
        self.monthly_table.setColumnWidth(2, 60)
        self.monthly_table.setColumnWidth(3, 80)
        
        header = self.monthly_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.monthly_table.setAlternatingRowColors(True)
        
        # Cargar datos mensuales
        self.load_monthly_analysis_data()
        
        layout.addWidget(self.monthly_table)
        
        return widget

    def change_period_view(self, period):
        """Cambiar la vista de período"""
        self.current_period = period
        
        # Actualizar estilos de botones
        self.day_btn.setStyleSheet(self.get_period_button_style(period == "day"))
        self.week_btn.setStyleSheet(self.get_period_button_style(period == "week"))
        self.month_btn.setStyleSheet(self.get_period_button_style(period == "month"))
        
        # Recargar datos
        self.load_period_summary_data()

    def load_period_summary_data(self):
        """Cargar datos del resumen por período"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            if self.current_period == "day":
                self.load_daily_summary(start_date, end_date)
            elif self.current_period == "week":
                self.load_weekly_summary(start_date, end_date)
            else:  # month
                self.load_monthly_summary(start_date, end_date)
                
        except Exception as e:
            print(f"❌ Error cargando resumen por período: {e}")

    def load_daily_summary(self, start_date, end_date):
        """Cargar resumen diario"""
        self.period_summary_table.setColumnCount(4)
        self.period_summary_table.setHorizontalHeaderLabels([
            "Fecha", "Ventas", "Órdenes", "Promedio"
        ])
        
        # Configurar anchos para vista diaria
        self.period_summary_table.setColumnWidth(0, 80)
        self.period_summary_table.setColumnWidth(1, 80)
        self.period_summary_table.setColumnWidth(2, 60)
        self.period_summary_table.setColumnWidth(3, 80)
        
        # Obtener datos por día
        current_date = start_date
        daily_data = []
        
        while current_date <= end_date:
            period_data = self.reports_ctrl.get_period_metrics(current_date, current_date)
            if period_data and period_data.get('total_orders', 0) > 0:
                daily_data.append({
                    'date': current_date.strftime("%d/%m"),
                    'sales': period_data.get('total_sales', 0.0),
                    'orders': period_data.get('total_orders', 0),
                    'avg_ticket': period_data.get('avg_ticket', 0.0)
                })
            current_date += timedelta(days=1)
        
        self.populate_period_table(daily_data)

    def load_weekly_summary(self, start_date, end_date):
        """Cargar resumen semanal"""
        self.period_summary_table.setColumnCount(4)
        self.period_summary_table.setHorizontalHeaderLabels([
            "Semana", "Ventas", "Órdenes", "Promedio"
        ])
        
        # Configurar anchos para vista semanal
        self.period_summary_table.setColumnWidth(0, 80)
        self.period_summary_table.setColumnWidth(1, 80)
        self.period_summary_table.setColumnWidth(2, 60)
        self.period_summary_table.setColumnWidth(3, 80)
        
        weekly_data = []
        current_date = start_date
        week_num = 1
        
        while current_date <= end_date:
            week_end = min(current_date + timedelta(days=6), end_date)
            period_data = self.reports_ctrl.get_period_metrics(current_date, week_end)
            
            if period_data and period_data.get('total_orders', 0) > 0:
                weekly_data.append({
                    'date': f"Sem {week_num}",
                    'sales': period_data.get('total_sales', 0.0),
                    'orders': period_data.get('total_orders', 0),
                    'avg_ticket': period_data.get('avg_ticket', 0.0)
                })
            
            current_date = week_end + timedelta(days=1)
            week_num += 1
        
        self.populate_period_table(weekly_data)

    def load_monthly_summary(self, start_date, end_date):
        """Cargar resumen mensual"""
        self.period_summary_table.setColumnCount(4)
        self.period_summary_table.setHorizontalHeaderLabels([
            "Mes", "Ventas", "Órdenes", "Promedio"
        ])
        
        # Configurar anchos para vista mensual
        self.period_summary_table.setColumnWidth(0, 80)
        self.period_summary_table.setColumnWidth(1, 80)
        self.period_summary_table.setColumnWidth(2, 60)
        self.period_summary_table.setColumnWidth(3, 80)
        
        monthly_data = []
        current_date = start_date.replace(day=1)
        
        while current_date <= end_date:
            # Último día del mes
            if current_date.month == 12:
                next_month = current_date.replace(year=current_date.year + 1, month=1)
            else:
                next_month = current_date.replace(month=current_date.month + 1)
            
            month_end = min((next_month - timedelta(days=1)), end_date)
            period_data = self.reports_ctrl.get_period_metrics(current_date, month_end)
            
            if period_data and period_data.get('total_orders', 0) > 0:
                monthly_data.append({
                    'date': current_date.strftime("%m/%Y"),
                    'sales': period_data.get('total_sales', 0.0),
                    'orders': period_data.get('total_orders', 0),
                    'avg_ticket': period_data.get('avg_ticket', 0.0)
                })
            
            current_date = next_month
        
        self.populate_period_table(monthly_data)

    def populate_period_table(self, data):
        """Poblar la tabla de períodos con datos"""
        if data:
            self.period_summary_table.setRowCount(len(data))
            
            for row, period in enumerate(data):
                # Período
                self.period_summary_table.setItem(row, 0, QTableWidgetItem(period['date']))
                
                # Ventas
                sales = period['sales']
                self.period_summary_table.setItem(row, 1, QTableWidgetItem(f"${sales:,.0f}"))
                
                # Órdenes
                self.period_summary_table.setItem(row, 2, QTableWidgetItem(str(period['orders'])))
                
                # Promedio
                avg = period['avg_ticket']
                self.period_summary_table.setItem(row, 3, QTableWidgetItem(f"${avg:,.0f}"))
        else:
            self.period_summary_table.setRowCount(1)
            self.period_summary_table.setItem(0, 0, QTableWidgetItem("No hay datos"))
            self.period_summary_table.setItem(0, 1, QTableWidgetItem("-"))
            self.period_summary_table.setItem(0, 2, QTableWidgetItem("-"))
            self.period_summary_table.setItem(0, 3, QTableWidgetItem("-"))

    def load_top_products_data(self):
        """Cargar datos de productos más vendidos"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            products_data = self.reports_ctrl.get_detailed_products_report(start_date, end_date)
            
            if products_data and len(products_data) > 0:
                # Limitar a top 10
                top_products = products_data[:10]
                self.top_products_table.setRowCount(len(top_products))
                
                total_revenue = sum(p.get('total_revenue', 0.0) for p in products_data)
                
                for row, product in enumerate(top_products):
                    # Nombre del producto
                    name = product.get('name', 'N/A')
                    if len(name) > 15:
                        name = name[:12] + "..."
                    self.top_products_table.setItem(row, 0, QTableWidgetItem(name))
                    
                    # Cantidad vendida
                    quantity = product.get('total_quantity', 0)
                    self.top_products_table.setItem(row, 1, QTableWidgetItem(str(quantity)))
                    
                    # Ingresos
                    revenue = product.get('total_revenue', 0.0)
                    self.top_products_table.setItem(row, 2, QTableWidgetItem(f"${revenue:,.0f}"))
                    
                    # Porcentaje del total
                    percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                    self.top_products_table.setItem(row, 3, QTableWidgetItem(f"{percentage:.1f}%"))
            else:
                self.top_products_table.setRowCount(1)
                self.top_products_table.setItem(0, 0, QTableWidgetItem("No hay datos"))
                self.top_products_table.setItem(0, 1, QTableWidgetItem("-"))
                self.top_products_table.setItem(0, 2, QTableWidgetItem("-"))
                self.top_products_table.setItem(0, 3, QTableWidgetItem("-"))
                
        except Exception as e:
            print(f"❌ Error cargando top productos: {e}")

    def load_monthly_analysis_data(self):
        """Cargar análisis mensual"""
        try:
            from datetime import datetime, date
            current_date = datetime.now()
            
            # Métricas del mes actual
            month_start = date(current_date.year, current_date.month, 1)
            month_end = date.today()
            
            month_data = self.reports_ctrl.get_period_metrics(month_start, month_end)
            
            if month_data:
                # Limpiar layout anterior
                while self.monthly_metrics_layout.count():
                    child = self.monthly_metrics_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                
                # Métricas del mes actual
                metrics = [
                    ("Ventas del Mes:", f"${month_data.get('total_sales', 0):,.0f}"),
                    ("Órdenes del Mes:", str(month_data.get('total_orders', 0))),
                    ("Promedio/Orden:", f"${month_data.get('avg_ticket', 0):,.0f}"),
                    ("Días Activos:", str(month_data.get('active_days', 0)))
                ]
                
                for i, (label_text, value_text) in enumerate(metrics):
                    label = QLabel(label_text)
                    label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 10px;")
                    
                    value = QLabel(value_text)
                    value.setStyleSheet(f"color: {ColorPalette.YINMN_BLUE}; font-size: 12px; font-weight: bold;")
                    
                    self.monthly_metrics_layout.addWidget(label, i // 2, (i % 2) * 2)
                    self.monthly_metrics_layout.addWidget(value, i // 2, (i % 2) * 2 + 1)
            
            # Comparación de últimos meses
            monthly_comparison = []
            for i in range(6):  # Últimos 6 meses
                if current_date.month - i <= 0:
                    month = current_date.month - i + 12
                    year = current_date.year - 1
                else:
                    month = current_date.month - i
                    year = current_date.year
                
                period_start = date(year, month, 1)
                if month == 12:
                    period_end = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    period_end = date(year, month + 1, 1) - timedelta(days=1)
                
                if period_end > date.today():
                    period_end = date.today()
                
                period_data = self.reports_ctrl.get_period_metrics(period_start, period_end)
                
                if period_data and period_data.get('total_orders', 0) > 0:
                    monthly_comparison.append({
                        'month': period_start.strftime("%m/%Y"),
                        'sales': period_data.get('total_sales', 0.0),
                        'orders': period_data.get('total_orders', 0),
                        'avg_ticket': period_data.get('avg_ticket', 0.0)
                    })
            
            # Poblar tabla de comparación
            if monthly_comparison:
                self.monthly_table.setRowCount(len(monthly_comparison))
                
                for row, data in enumerate(reversed(monthly_comparison)):  # Más reciente primero
                    self.monthly_table.setItem(row, 0, QTableWidgetItem(data['month']))
                    self.monthly_table.setItem(row, 1, QTableWidgetItem(f"${data['sales']:,.0f}"))
                    self.monthly_table.setItem(row, 2, QTableWidgetItem(str(data['orders'])))
                    self.monthly_table.setItem(row, 3, QTableWidgetItem(f"${data['avg_ticket']:,.0f}"))
            else:
                self.monthly_table.setRowCount(1)
                self.monthly_table.setItem(0, 0, QTableWidgetItem("No hay datos"))
                self.monthly_table.setItem(0, 1, QTableWidgetItem("-"))
                self.monthly_table.setItem(0, 2, QTableWidgetItem("-"))
                self.monthly_table.setItem(0, 3, QTableWidgetItem("-"))
                
        except Exception as e:
            print(f"❌ Error cargando análisis mensual: {e}")

    def clear_right_panel_content(self):
        """Limpiar el contenido del panel derecho"""
        # Eliminar todos los widgets del layout de contenido
        while self.right_content_layout.count():
            child = self.right_content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def toggle_detailed_view(self):
        """Alternar entre vista principal y detallada"""
        if self.current_mode == "main":
            self.show_detailed_view()
        else:
            self.show_main_view()

    def show_detailed_view(self):
        """Mostrar análisis detallado"""
        self.clear_right_panel_content()
        self.current_mode = "detailed"
        
        # Título más compacto
        title = QLabel("📋 Análisis Detallado")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        self.right_content_layout.addWidget(title)
        
        # Crear tabs para diferentes análisis
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(self.get_tab_style())
        
        # Tab de productos
        products_tab = self.create_products_analysis_tab()
        tab_widget.addTab(products_tab, "🍽️ Productos")
        
        # Tab de períodos
        periods_tab = self.create_periods_analysis_tab()
        tab_widget.addTab(periods_tab, "📅 Períodos")
        
        # Tab de estadísticas
        stats_tab = self.create_statistics_tab()
        tab_widget.addTab(stats_tab, "📊 Stats")
        
        self.right_content_layout.addWidget(tab_widget)
        
        # Actualizar el botón
        self.details_btn.setText("📊 Resumen")
        
        print("✅ Modo detallado activado")

    def create_products_analysis_tab(self):
        """Crear tab de análisis de productos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        
        # Título más compacto
        title_label = QLabel("🏆 Productos Más Vendidos")
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        title_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 5px;")
        layout.addWidget(title_label)
        
        # Tabla de productos más vendidos
        products_table = QTableWidget()
        products_table.setStyleSheet(self.get_table_style())
        
        # Configurar columnas
        products_table.setColumnCount(4)
        products_table.setHorizontalHeaderLabels([
            "Producto", "Cant.", "Ingresos", "%"
        ])
        
        # Configurar tabla para pantallas pequeñas
        header = products_table.horizontalHeader()
        header.setStretchLastSection(True)
        products_table.setAlternatingRowColors(True)
        products_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        products_table.verticalHeader().setVisible(False)
        
        # Ajustar ancho de columnas
        products_table.setColumnWidth(0, 120)  # Producto
        products_table.setColumnWidth(1, 50)   # Cantidad
        products_table.setColumnWidth(2, 80)   # Ingresos
        products_table.setColumnWidth(3, 40)   # Porcentaje
        
        # Cargar datos
        self.load_products_data(products_table)
        
        layout.addWidget(products_table)
        
        return widget

    def create_periods_analysis_tab(self):
        """Crear tab de análisis por períodos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        
        # Título más compacto
        title_label = QLabel("📅 Ventas por Período")
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        title_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 5px;")
        layout.addWidget(title_label)
        
        # Tabla de ventas por día
        periods_table = QTableWidget()
        periods_table.setStyleSheet(self.get_table_style())
        
        # Configurar columnas
        periods_table.setColumnCount(4)
        periods_table.setHorizontalHeaderLabels([
            "Fecha", "Órdenes", "Ventas", "Promedio"
        ])
        
        # Configurar tabla para pantallas pequeñas
        header = periods_table.horizontalHeader()
        header.setStretchLastSection(True)
        periods_table.setAlternatingRowColors(True)
        periods_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        periods_table.verticalHeader().setVisible(False)
        
        # Ajustar ancho de columnas
        periods_table.setColumnWidth(0, 70)   # Fecha
        periods_table.setColumnWidth(1, 50)   # Órdenes
        periods_table.setColumnWidth(2, 80)   # Ventas
        periods_table.setColumnWidth(3, 80)   # Promedio
        
        # Cargar datos
        self.load_periods_data(periods_table)
        
        layout.addWidget(periods_table)
        
        return widget

    def create_statistics_tab(self):
        """Crear tab de estadísticas generales"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        
        # Frame de estadísticas más compacto
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.StyledPanel)
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 10px;
            }}
        """)
        
        stats_layout = QGridLayout(stats_frame)
        stats_layout.setSpacing(5)
        stats_layout.setVerticalSpacing(3)
        
        # Cargar y mostrar estadísticas
        self.load_statistics(stats_layout)
        
        layout.addWidget(stats_frame)
        layout.addStretch()
        
        return widget

    def load_products_data(self, table):
        """Cargar datos de productos en la tabla"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            products_data = self.reports_ctrl.get_detailed_products_report(start_date, end_date)
            
            if products_data and len(products_data) > 0:
                table.setRowCount(len(products_data))
                
                for row, product in enumerate(products_data):
                    # Nombre del producto
                    table.setItem(row, 0, QTableWidgetItem(str(product.get('name', 'N/A'))))
                    
                    # Cantidad vendida
                    quantity = product.get('total_quantity', 0)
                    table.setItem(row, 1, QTableWidgetItem(str(quantity)))
                    
                    # Ingresos
                    revenue = product.get('total_revenue', 0.0)
                    table.setItem(row, 2, QTableWidgetItem(f"${revenue:,.0f}"))
                    
                    # Porcentaje del total (calculado)
                    total_revenue = sum(p.get('total_revenue', 0.0) for p in products_data)
                    percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                    table.setItem(row, 3, QTableWidgetItem(f"{percentage:.1f}%"))
            else:
                table.setRowCount(1)
                table.setItem(0, 0, QTableWidgetItem("No hay datos disponibles"))
                table.setItem(0, 1, QTableWidgetItem("-"))
                table.setItem(0, 2, QTableWidgetItem("-"))
                table.setItem(0, 3, QTableWidgetItem("-"))
                
        except Exception as e:
            print(f"❌ Error cargando datos de productos: {e}")
            table.setRowCount(1)
            table.setItem(0, 0, QTableWidgetItem("Error cargando datos"))

    def load_periods_data(self, table):
        """Cargar datos de períodos en la tabla"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Obtener datos por día
            current_date = start_date
            periods_data = []
            
            while current_date <= end_date:
                period_data = self.reports_ctrl.get_period_metrics(current_date, current_date)
                if period_data:
                    periods_data.append({
                        'date': current_date,
                        'orders': period_data.get('total_orders', 0),
                        'sales': period_data.get('total_sales', 0.0),
                        'avg_ticket': period_data.get('avg_ticket', 0.0)
                    })
                current_date += timedelta(days=1)
            
            if periods_data:
                table.setRowCount(len(periods_data))
                
                for row, period in enumerate(periods_data):
                    # Fecha
                    date_str = period['date'].strftime("%d/%m/%Y")
                    table.setItem(row, 0, QTableWidgetItem(date_str))
                    
                    # Órdenes
                    table.setItem(row, 1, QTableWidgetItem(str(period['orders'])))
                    
                    # Ventas
                    sales = period['sales']
                    table.setItem(row, 2, QTableWidgetItem(f"${sales:,.0f}"))
                    
                    # Ticket promedio
                    avg_ticket = period['avg_ticket']
                    table.setItem(row, 3, QTableWidgetItem(f"${avg_ticket:,.0f}"))
            else:
                table.setRowCount(1)
                table.setItem(0, 0, QTableWidgetItem("No hay datos disponibles"))
                table.setItem(0, 1, QTableWidgetItem("-"))
                table.setItem(0, 2, QTableWidgetItem("-"))
                table.setItem(0, 3, QTableWidgetItem("-"))
                
        except Exception as e:
            print(f"❌ Error cargando datos de períodos: {e}")
            table.setRowCount(1)
            table.setItem(0, 0, QTableWidgetItem("Error cargando datos"))

    def load_statistics(self, layout):
        """Cargar estadísticas generales"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Obtener estadísticas
            stats = self.reports_ctrl.get_general_statistics(start_date, end_date)
            
            if stats:
                row = 0
                for key, value in stats.items():
                    # Etiqueta más compacta
                    label = QLabel(f"{key}:")
                    label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 10px;")
                    label.setWordWrap(True)
                    layout.addWidget(label, row, 0)
                    
                    # Valor
                    if isinstance(value, float):
                        if 'porcentaje' in key.lower() or '%' in str(value):
                            value_text = f"{value:.1f}%"
                        elif 'precio' in key.lower() or 'dinero' in key.lower():
                            value_text = f"${value:,.0f}"
                        else:
                            value_text = f"{value:.2f}"
                    else:
                        value_text = str(value)
                    
                    value_label = QLabel(value_text)
                    value_label.setStyleSheet(f"color: {ColorPalette.YINMN_BLUE}; font-size: 11px; font-weight: bold;")
                    value_label.setWordWrap(True)
                    layout.addWidget(value_label, row, 1)
                    
                    row += 1
            else:
                no_data_label = QLabel("No hay estadísticas disponibles")
                no_data_label.setStyleSheet(f"color: {ColorPalette.OXFORD_BLUE}; font-size: 10px;")
                no_data_label.setWordWrap(True)
                layout.addWidget(no_data_label, 0, 0, 1, 2)
                
        except Exception as e:
            print(f"❌ Error cargando estadísticas: {e}")
            error_label = QLabel("Error cargando estadísticas")
            error_label.setStyleSheet(f"color: {ColorPalette.ERROR}; font-size: 10px;")
            error_label.setWordWrap(True)
            layout.addWidget(error_label, 0, 0, 1, 2)

    def set_date_range(self, days):
        """Establecer rango de fechas"""
        end_date = QDate.currentDate()
        if days == 0:
            start_date = end_date
        else:
            start_date = end_date.addDays(-days)
        
        self.start_date.setDate(start_date)
        self.end_date.setDate(end_date)

    def refresh_data(self):
        """Actualizar todos los datos"""
        print("🔄 Actualizando datos de reportes...")
        
        # Cargar métricas principales
        self.load_main_metrics()
        
        # Si estamos en modo principal, actualizar las tablas principales
        if self.current_mode == "main":
            if hasattr(self, 'period_summary_table'):
                self.load_period_summary_data()
            if hasattr(self, 'top_products_table'):
                self.load_top_products_data()
            if hasattr(self, 'monthly_table'):
                self.load_monthly_analysis_data()
        
        print("✅ Datos actualizados")

    def load_main_metrics(self):
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
                
                # Si no hay datos reales, mostrar ceros en lugar de datos falsos
                if total_orders == 0:
                    print("ℹ️  No hay datos de ventas - mostrando métricas en cero")
                
                # Actualizar labels con formato colombiano más compacto
                self.sales_value.setText(f"${total_sales:,.0f}")
                self.orders_value.setText(str(total_orders))
                self.avg_value.setText(f"${avg_ticket:,.0f}")
                self.margin_value.setText(f"{overall_margin:.1f}%")
                
            else:
                # No hay datos - mostrar ceros
                self.sales_value.setText("$0")
                self.orders_value.setText("0")
                self.avg_value.setText("$0")
                self.margin_value.setText("0%")
                
        except Exception as e:
            print(f"❌ Error cargando métricas: {e}")
            self.sales_value.setText("Error")
            self.orders_value.setText("Error")
            self.avg_value.setText("Error")
            self.margin_value.setText("Error")

    def export_report(self):
        """Exportar reporte completo a CSV"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Crear nombre de archivo
            filename = f"reporte_completo_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
            
            # Abrir diálogo para guardar archivo
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Exportar Reporte Completo", 
                filename, 
                "CSV files (*.csv)"
            )
            
            if file_path:
                # Obtener datos
                sales_summary = self.reports_ctrl.get_sales_summary(start_date, end_date)
                products_data = self.reports_ctrl.get_detailed_products_report(start_date, end_date)
                monthly_data = self.reports_ctrl.get_daily_sales(start_date, end_date)
                
                # Escribir CSV
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Encabezado del reporte
                    writer.writerow(['REPORTE COMPLETO DE VENTAS'])
                    writer.writerow([f'Período: {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}'])
                    writer.writerow([f'Fecha de generación: {datetime.now().strftime("%d/%m/%Y %H:%M")}'])
                    writer.writerow([])
                    
                    # Resumen general
                    writer.writerow(['RESUMEN EJECUTIVO'])
                    if sales_summary:
                        total_sales = sales_summary.get('total_sales', 0)
                        total_orders = sales_summary.get('total_orders', 0)
                        avg_ticket = sales_summary.get('avg_ticket', 0)
                        
                        writer.writerow(['Total Ventas', f"${total_sales:,.0f} COP"])
                        writer.writerow(['Total Órdenes', total_orders])
                        writer.writerow(['Ticket Promedio', f"${avg_ticket:,.0f} COP"])
                        
                        # Calcular días del período para promedio diario
                        days = (end_date - start_date).days + 1
                        avg_daily_sales = total_sales / days if days > 0 else 0
                        avg_daily_orders = total_orders / days if days > 0 else 0
                        
                        writer.writerow(['Promedio Ventas Diarias', f"${avg_daily_sales:,.0f} COP"])
                        writer.writerow(['Promedio Órdenes Diarias', f"{avg_daily_orders:.1f}"])
                    writer.writerow([])
                    
                    # Top 5 productos más vendidos
                    writer.writerow(['TOP 5 PRODUCTOS MÁS VENDIDOS'])
                    writer.writerow(['Posición', 'Producto', 'Cantidad Vendida', 'Ingresos (COP)', '% del Total', 'Categoría'])
                    
                    if products_data:
                        total_revenue = sum(p.get('total_revenue', 0.0) for p in products_data)
                        top_5_products = products_data[:5]
                        
                        for i, product in enumerate(top_5_products, 1):
                            name = product.get('name', 'N/A')
                            quantity = product.get('total_quantity', 0)
                            revenue = product.get('total_revenue', 0.0)
                            percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                            category = product.get('category', 'N/A')
                            
                            writer.writerow([
                                f"#{i}", 
                                name, 
                                quantity, 
                                f"{revenue:,.0f}", 
                                f"{percentage:.1f}%",
                                category
                            ])
                    writer.writerow([])
                    
                    # Resumen por días/meses
                    if monthly_data:
                        writer.writerow(['VENTAS POR DÍA'])
                        writer.writerow(['Fecha', 'Ventas (COP)', 'Órdenes', 'Ticket Promedio'])
                        
                        for day_data in monthly_data:
                            date_str = day_data.get('date', 'N/A')
                            daily_sales = day_data.get('total_sales', 0)
                            daily_orders = day_data.get('total_orders', 0)
                            daily_avg = daily_sales / daily_orders if daily_orders > 0 else 0
                            
                            writer.writerow([
                                date_str,
                                f"{daily_sales:,.0f}",
                                daily_orders,
                                f"{daily_avg:,.0f}"
                            ])
                        writer.writerow([])
                    
                    # Productos completos para referencia
                    writer.writerow(['DETALLE COMPLETO DE PRODUCTOS'])
                    writer.writerow(['Producto', 'Categoría', 'Cantidad', 'Ingresos (COP)', 'Órdenes', 'Precio Promedio'])
                    
                    if products_data:
                        for product in products_data:
                            name = product.get('name', 'N/A')
                            category = product.get('category', 'N/A')
                            quantity = product.get('total_quantity', 0)
                            revenue = product.get('total_revenue', 0.0)
                            orders = product.get('orders_count', 0)
                            avg_price = product.get('avg_unit_price', 0.0)
                            
                            writer.writerow([
                                name, 
                                category,
                                quantity, 
                                f"{revenue:,.0f}", 
                                orders,
                                f"{avg_price:,.0f}"
                            ])
                
                QMessageBox.information(self, "Éxito", f"Reporte completo exportado exitosamente a:\n{file_path}")
                
        except Exception as e:
            print(f"❌ Error exportando reporte: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error al exportar reporte:\n{str(e)}")

    # Métodos de estilo
    def get_date_edit_style(self):
        return f"""
            QDateEdit {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 11px;
                color: {ColorPalette.RICH_BLACK};
                min-height: 20px;
                max-height: 20px;
            }}
            QDateEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
                border-width: 2px;
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 18px;
                border-left: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
            }}
            QDateEdit::down-arrow {{
                image: none;
                border: none;
                width: 10px;
                height: 10px;
            }}
        """

    def get_small_button_style(self):
        return f"""
            QPushButton {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 10px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                min-height: 18px;
                max-height: 18px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: white;
                border-color: {ColorPalette.YINMN_BLUE};
            }}
            QPushButton:pressed {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """

    def get_primary_button_style(self):
        return f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                font-weight: bold;
                color: white;
                min-height: 22px;
                max-height: 22px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
            QPushButton:pressed {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
            }}
        """

    def get_secondary_button_style(self):
        return f"""
            QPushButton {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                min-height: 22px;
                max-height: 22px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: white;
                border-color: {ColorPalette.YINMN_BLUE};
            }}
            QPushButton:pressed {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """

    def get_table_style(self):
        return f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                gridline-color: {ColorPalette.SILVER_LAKE_BLUE};
                selection-background-color: {ColorPalette.SILVER_LAKE_BLUE};
                font-size: 10px;
            }}
            QTableWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                min-height: 18px;
            }}
            QTableWidget::item:selected {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 10px;
                min-height: 20px;
            }}
        """

    def get_tab_style(self):
        return f"""
            QTabWidget::pane {{
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-bottom: none;
                padding: 6px 12px;
                margin-right: 1px;
                color: {ColorPalette.RICH_BLACK};
                font-size: 10px;
                min-height: 16px;
            }}
            QTabBar::tab:selected {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: white;
                font-weight: bold;
            }}
            QTabBar::tab:hover {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
            }}
        """

    def get_period_button_style(self, is_selected):
        """Obtener estilo para botones de período"""
        if is_selected:
            return f"""
                QPushButton {{
                    background-color: {ColorPalette.YINMN_BLUE};
                    border: 1px solid {ColorPalette.YINMN_BLUE};
                    border-radius: 4px;
                    padding: 4px 12px;
                    font-size: 10px;
                    font-weight: bold;
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.OXFORD_BLUE};
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: white;
                    border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                    border-radius: 4px;
                    padding: 4px 12px;
                    font-size: 10px;
                    font-weight: bold;
                    color: {ColorPalette.RICH_BLACK};
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.SILVER_LAKE_BLUE};
                    color: white;
                }}
            """
