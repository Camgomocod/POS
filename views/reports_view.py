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
        
        # Controles de fecha
        date_frame = self.create_date_controls()
        layout.addWidget(date_frame)
        
        # Métricas principales
        metrics_frame = self.create_metrics_frame()
        layout.addWidget(metrics_frame)
        
        # Botones de acción
        buttons_frame = self.create_action_buttons()
        layout.addWidget(buttons_frame)
        
        # Espaciador
        layout.addStretch()
        
        return panel

    def create_date_controls(self):
        """Crear controles de fecha"""
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
        
        # Título más pequeño
        title = QLabel("📅 Período")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 3px;")
        layout.addWidget(title)
        
        # Fecha inicio
        start_layout = QHBoxLayout()
        start_layout.setSpacing(5)
        start_label = QLabel("Desde:")
        start_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 10px;")
        start_label.setMinimumWidth(40)
        start_label.setMaximumWidth(40)
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.start_date.setStyleSheet(self.get_date_edit_style())
        self.start_date.setMinimumHeight(25)
        self.start_date.setMaximumHeight(25)
        self.start_date.dateChanged.connect(self.refresh_data)
        
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_date)
        layout.addLayout(start_layout)
        
        # Fecha fin
        end_layout = QHBoxLayout()
        end_layout.setSpacing(5)
        end_label = QLabel("Hasta:")
        end_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold; font-size: 10px;")
        end_label.setMinimumWidth(40)
        end_label.setMaximumWidth(40)
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setStyleSheet(self.get_date_edit_style())
        self.end_date.setMinimumHeight(25)
        self.end_date.setMaximumHeight(25)
        self.end_date.dateChanged.connect(self.refresh_data)
        
        end_layout.addWidget(end_label)
        end_layout.addWidget(self.end_date)
        layout.addLayout(end_layout)
        
        # Botones de períodos rápidos
        quick_buttons_layout = QHBoxLayout()
        quick_buttons_layout.setSpacing(3)
        
        today_btn = QPushButton("Hoy")
        today_btn.clicked.connect(lambda: self.set_date_range(0))
        today_btn.setStyleSheet(self.get_small_button_style())
        today_btn.setMaximumHeight(22)
        
        week_btn = QPushButton("7d")
        week_btn.clicked.connect(lambda: self.set_date_range(7))
        week_btn.setStyleSheet(self.get_small_button_style())
        week_btn.setMaximumHeight(22)
        
        month_btn = QPushButton("30d")
        month_btn.clicked.connect(lambda: self.set_date_range(30))
        month_btn.setStyleSheet(self.get_small_button_style())
        month_btn.setMaximumHeight(22)
        
        quick_buttons_layout.addWidget(today_btn)
        quick_buttons_layout.addWidget(week_btn)
        quick_buttons_layout.addWidget(month_btn)
        layout.addLayout(quick_buttons_layout)
        
        return frame

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
        self.sales_value = QLabel("$0 COP")
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
        self.avg_value = QLabel("$0 COP")
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
        """Mostrar la vista principal (sin gráficos)"""
        self.clear_right_panel_content()
        self.current_mode = "main"
        
        # Título más compacto
        title = QLabel("📊 Resumen de Ventas")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        self.right_content_layout.addWidget(title)
        
        # Actualizar el botón
        self.details_btn.setText("📋 Detallado")
        
        print("✅ Modo principal activado")

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
        
        # Si estamos en modo detallado, actualizar también esas vistas
        if self.current_mode == "detailed":
            # Aquí se actualizarían las tablas del modo detallado
            pass
        
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
        """Exportar reporte a CSV"""
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()
            
            # Crear nombre de archivo
            filename = f"reporte_ventas_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
            
            # Abrir diálogo para guardar archivo
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Exportar Reporte", 
                filename, 
                "CSV files (*.csv)"
            )
            
            if file_path:
                # Obtener datos
                sales_summary = self.reports_ctrl.get_sales_summary(start_date, end_date)
                products_data = self.reports_ctrl.get_detailed_products_report(start_date, end_date)
                
                # Escribir CSV
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Encabezado del reporte
                    writer.writerow(['REPORTE DE VENTAS'])
                    writer.writerow([f'Período: {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}'])
                    writer.writerow([])
                    
                    # Resumen general
                    writer.writerow(['RESUMEN GENERAL'])
                    if sales_summary:
                        writer.writerow(['Total Ventas', f"${sales_summary.get('total_sales', 0):,.0f} COP"])
                        writer.writerow(['Total Órdenes', sales_summary.get('total_orders', 0)])
                        writer.writerow(['Ticket Promedio', f"${sales_summary.get('avg_ticket', 0):,.0f} COP"])
                    writer.writerow([])
                    
                    # Productos detallados
                    writer.writerow(['PRODUCTOS MÁS VENDIDOS'])
                    writer.writerow(['Producto', 'Cantidad', 'Ingresos (COP)', 'Porcentaje'])
                    
                    if products_data:
                        total_revenue = sum(p.get('total_revenue', 0.0) for p in products_data)
                        for product in products_data:
                            name = product.get('name', 'N/A')
                            quantity = product.get('total_quantity', 0)
                            revenue = product.get('total_revenue', 0.0)
                            percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                            
                            writer.writerow([name, quantity, f"{revenue:,.0f}", f"{percentage:.1f}%"])
                
                QMessageBox.information(self, "Éxito", f"Reporte exportado exitosamente a:\n{file_path}")
                
        except Exception as e:
            print(f"❌ Error exportando reporte: {e}")
            QMessageBox.critical(self, "Error", f"Error al exportar reporte:\n{str(e)}")

    # Métodos de estilo
    def get_date_edit_style(self):
        return f"""
            QDateEdit {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 10px;
                color: {ColorPalette.RICH_BLACK};
                min-height: 18px;
                max-height: 18px;
            }}
            QDateEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
            }}
            QDateEdit::down-arrow {{
                image: none;
                border: none;
            }}
        """

    def get_small_button_style(self):
        return f"""
            QPushButton {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                padding: 3px 8px;
                font-size: 9px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                min-height: 16px;
                max-height: 16px;
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
