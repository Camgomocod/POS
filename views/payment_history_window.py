# views/payment_history_window.py
import sys
import os
from datetime import datetime, date, timedelta
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
                             QDateEdit, QLineEdit, QComboBox, QSpinBox, QDialog,
                             QFormLayout, QTextEdit, QMessageBox, QProgressBar,
                             QFileDialog, QScrollArea, QSizePolicy, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QThread, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QColor
from controllers.payment_controller import PaymentController
from models.order import OrderStatus
from utils.colors import ColorPalette, CommonStyles

class PaymentDetailDialog(QDialog):
    """Dialog mejorado para mostrar detalles completos de un pago"""
    
    def __init__(self, order, parent=None):
        super().__init__(parent)
        self.order = order
        self.setWindowTitle(f"Detalle del Pago - Orden #{order.id}")
        self.setFixedSize(500, 450)  # Tamaño optimizado para laptop
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        # Layout principal con espaciado optimizado
        layout = QVBoxLayout(self)
        layout.setSpacing(6)  # Espaciado entre elementos
        layout.setContentsMargins(12, 12, 12, 12)  # Márgenes consistentes
        
        # Header compacto con información principal
        header_frame = QFrame()
        header_frame.setFixedHeight(65)  # Altura fija para el header (aumentada +5)
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 8px;
                border: 1px solid {ColorPalette.OXFORD_BLUE};
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 8, 8, 8)
        header_layout.setSpacing(5)
        
        # Título principal
        title = QLabel(f"🧾 ORDEN #{self.order.id}")
        title.setStyleSheet(f"""
            font-size: 16px; 
            font-weight: bold; 
            color: {ColorPalette.PLATINUM};
        """)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Fecha y estado en una línea
        info_layout = QHBoxLayout()
        info_layout.setSpacing(5)
        
        date_label = QLabel(self.order.created_at.strftime('%d/%m/%Y %H:%M'))
        date_label.setStyleSheet(f"""
            color: {ColorPalette.PLATINUM};
            font-size: 14px;
            font-weight: bold;
        """)
        info_layout.addWidget(date_label)
        
        info_layout.addStretch()
        
        status_label = QLabel(self.order.status_display)
        status_label.setStyleSheet(f"""
            background-color: {ColorPalette.SUCCESS};
            color: {ColorPalette.PLATINUM};
            padding: 2px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 13px;
        """)
        info_layout.addWidget(status_label)
        
        header_layout.addLayout(info_layout)
        layout.addWidget(header_frame)
        
        # Información del cliente compacta
        customer_frame = QFrame()
        customer_frame.setFixedHeight(60)  # Altura fija (aumentada +5)
        customer_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 6px;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
            }}
        """)
        customer_layout = QVBoxLayout(customer_frame)
        customer_layout.setContentsMargins(8, 6, 8, 6)
        customer_layout.setSpacing(8)
        
        # Información en líneas horizontales compactas
        customer_info_layout = QHBoxLayout()
        customer_info = QLabel(f"👤 {self.order.customer_name}")
        customer_info.setStyleSheet(f"font-size: 15px; color: {ColorPalette.RICH_BLACK}; font-weight: bold;")
        customer_info_layout.addWidget(customer_info)
        customer_info_layout.addStretch()
        
        table_info = f"Mesa {self.order.table_number}" if self.order.table_number else "Para llevar"
        location_info = QLabel(f"📍 {table_info}")
        location_info.setStyleSheet(f"font-size: 14px; color: {ColorPalette.SILVER_LAKE_BLUE};")
        customer_info_layout.addWidget(location_info)
        customer_layout.addLayout(customer_info_layout)
        
        # Método de pago
        payment_info = QLabel(f"💳 Pago: {(self.order.payment_method or 'donddoo').capitalize()}")
        payment_info.setStyleSheet(f"font-size: 14px; color: {ColorPalette.RICH_BLACK};")
        customer_layout.addWidget(payment_info)
        
        layout.addWidget(customer_frame)
        
        # Productos con diseño muy simplificado
        products_title = QLabel("🛍️ PRODUCTOS")
        products_title.setStyleSheet(f"""
            font-size: 18px; 
            font-weight: bold; 
            color: {ColorPalette.RICH_BLACK};
            padding: 5px;
        """)
        layout.addWidget(products_title)
        
        # Área de productos con scroll personalizada
        products_scroll = QScrollArea()
        products_scroll.setFixedHeight(180)  # Altura fija para evitar overflow
        products_scroll.setWidgetResizable(True)
        products_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        products_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        products_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                background-color: {ColorPalette.PLATINUM};
            }}
            QScrollBar:vertical {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                min-height: 20px;
            }}
        """)
        
        # Widget contenedor de productos
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)
        products_layout.setContentsMargins(8, 8, 8, 8)
        products_layout.setSpacing(3)
        
        # Mostrar todos los productos con scroll
        for item in self.order.items:
            item_frame = QFrame()
            item_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)};
                    border-radius: 4px;
                    padding: 2px;
                }}
            """)
            item_layout = QHBoxLayout(item_frame)
            item_layout.setContentsMargins(4, 2, 4, 2)
            item_layout.setSpacing(5)
            
            # Nombre del producto (expandible)
            product_info = QLabel(f"{item.product.name}")
            product_info.setStyleSheet(f"font-size: 16px; color: {ColorPalette.RICH_BLACK}; font-weight: bold;")
            product_info.setWordWrap(True)
            item_layout.addWidget(product_info, 1)  # Factor de expansión
            
            # Cantidad y precio
            qty_price = QLabel(f"{item.quantity}x")
            qty_price.setStyleSheet(f"font-size: 16px; color: {ColorPalette.SILVER_LAKE_BLUE}; font-weight: bold;")
            qty_price.setFixedWidth(60)
            item_layout.addWidget(qty_price)
            
            price_label = QLabel(f"$ {item.unit_price:,.0f}")
            price_label.setStyleSheet(f"font-size: 16px; color: {ColorPalette.SILVER_LAKE_BLUE};")
            price_label.setFixedWidth(90)
            price_label.setAlignment(Qt.AlignRight)
            item_layout.addWidget(price_label)
            
            # Subtotal
            subtotal_label = QLabel(f"$ {item.subtotal:,.0f}")
            subtotal_label.setStyleSheet(f"""
                font-weight: bold; 
                color: {ColorPalette.SUCCESS}; 
                font-size: 14px;
            """)
            subtotal_label.setFixedWidth(90)
            subtotal_label.setAlignment(Qt.AlignRight)
            item_layout.addWidget(subtotal_label)
            
            products_layout.addWidget(item_frame)
        
        # Espaciador al final para evitar que los elementos se estiren
        products_layout.addStretch()
        
        products_scroll.setWidget(products_widget)
        layout.addWidget(products_scroll)
        
        # Total final
        total_frame = QFrame()
        total_frame.setFixedHeight(40)  # Altura fija (aumentada +5)
        total_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.SUCCESS};
                border-radius: 6px;
            }}
        """)
        total_layout = QHBoxLayout(total_frame)
        total_layout.setContentsMargins(10, 5, 10, 5)
        
        total_label = QLabel(f"💰 TOTAL: ${self.order.total:,.0f}")
        total_label.setStyleSheet(f"""
            font-size: 18px; 
            font-weight: bold; 
            color: {ColorPalette.PLATINUM};
        """)
        total_label.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(total_label)
        
        layout.addWidget(total_frame)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        close_btn = QPushButton("❌ Cerrar")
        close_btn.setFixedSize(90, 32)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)
        
        print_btn = QPushButton("🖨️ Reimprimir")
        print_btn.setFixedSize(110, 32)
        print_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        print_btn.clicked.connect(self.reprint_receipt)
        buttons_layout.addWidget(print_btn)
        
        layout.addLayout(buttons_layout)
        
        # Estilo general del diálogo simplificado
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 10px;
            }}
        """)
        
    def reprint_receipt(self):
        """Reimprimir recibo con mejor manejo de errores"""
        try:
            from utils.printer import ReceiptPrinter
            printer = ReceiptPrinter()
            
            # Convertir order items a formato esperado
            cart_items = []
            for item in self.order.items:
                cart_items.append({
                    'product': item.product,
                    'quantity': item.quantity
                })
            
            printer.print_receipt(self.order, cart_items)
            
            # Mostrar mensaje de éxito mejorado
            msg = QMessageBox(self)
            msg.setWindowTitle("Impresión Exitosa")
            msg.setText("✅ El recibo se ha enviado a impresión correctamente")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {ColorPalette.PLATINUM};
                }}
                QMessageBox QLabel {{
                    color: {ColorPalette.RICH_BLACK};
                    font-size: 16px;
                }}
            """)
            msg.exec_()
            
        except Exception as e:
            # Mostrar error mejorado
            msg = QMessageBox(self)
            msg.setWindowTitle("Error de Impresión")
            msg.setText(f"❌ Error al imprimir el recibo:\n\n{str(e)}")
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {ColorPalette.PLATINUM};
                }}
                QMessageBox QLabel {{
                    color: {ColorPalette.RICH_BLACK};
                    font-size: 16px;
                }}
            """)
            msg.exec_()

class ExportThread(QThread):
    """Thread para exportar datos sin bloquear la UI"""
    
    finished = pyqtSignal(str)  # Ruta del archivo generado
    error = pyqtSignal(str)     # Mensaje de error
    
    def __init__(self, serialized_orders, filepath):
        super().__init__()
        self.serialized_orders = serialized_orders
        self.filepath = filepath
    
    def run(self):
        try:
            import pandas as pd
            from datetime import datetime
            import os
            
            # Preparar datos para Excel
            data = []
            for order in self.serialized_orders:
                # Información básica de la orden
                base_info = {
                    'Fecha': order['created_at'].strftime('%d/%m/%Y'),
                    'Hora': order['created_at'].strftime('%H:%M:%S'),
                    'Orden #': order['id'],
                    'Cliente': order['customer_name'],
                    'Mesa': order['table_number'] if order['table_number'] else 'Para llevar',
                    'Estado': order['status_display'],
                    'Total': order['total'],
                    'Método Pago': (order['payment_method'] or 'Efectivo').capitalize(),
                    'Cajero': 'Sistema'  # Por ahora valor fijo
                }
                
                # Agregar información de productos
                if order['items']:
                    products_info = []
                    for item in order['items']:
                        products_info.append(
                            f"{item['quantity']}x {item['product_name']} (${item['unit_price']:.2f})"
                        )
                    base_info['Productos'] = '; '.join(products_info)
                else:
                    base_info['Productos'] = 'N/A'
                
                data.append(base_info)
            
            # Crear DataFrame y exportar
            df = pd.DataFrame(data)
            
            # Reorganizar columnas
            columns_order = [
                'Fecha', 'Hora', 'Orden #', 'Cliente', 'Mesa', 
                'Productos', 'Total', 'Método Pago', 'Cajero', 'Estado'
            ]
            df = df[columns_order]
            
            # Asegurar que el directorio existe
            directory = os.path.dirname(self.filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # Exportar a Excel
            df.to_excel(self.filepath, index=False, sheet_name='Historial de Pagos')
            
            self.finished.emit(os.path.abspath(self.filepath))
        except Exception as e:
            self.error.emit(str(e))

class PaymentHistoryView(QWidget):
    """Vista para el historial de pagos con diseño optimizado"""
    
    back_to_pos = pyqtSignal()  # Señal para volver a POS
    open_kitchen = pyqtSignal()  # Señal para abrir cocina
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.payment_controller = PaymentController()
        self.current_page = 1
        self.page_size = 15  # Reducido para mejor rendimiento visual
        self.current_orders = []
        self.init_ui()
        # No cargar datos automáticamente en __init__
        # self.load_payment_history()
    
    def refresh_data(self):
        """Refrescar datos del historial - método público para llamar desde fuera"""
        # Refrescar controlador para obtener datos más recientes de la BD
        self.payment_controller = PaymentController()
        self.current_page = 1  # Resetear a primera página
        self.load_payment_history()
    
    def force_refresh(self):
        """Forzar actualización de datos (alias para refresh_data)"""
        self.refresh_data()
    
    def showEvent(self, event):
        """Se ejecuta cuando se muestra la vista"""
        super().showEvent(event)
        # Refrescar datos cada vez que se muestra la vista
        # Solo si ya se ha inicializado completamente
        if hasattr(self, 'payment_controller'):
            # Refrescar controlador para obtener datos más recientes
            self.payment_controller = PaymentController()
            # Resetear a primera página y refrescar
            self.current_page = 1
            self.refresh_data()
    
    def init_ui(self):
        # Detectar resolución para diseño responsivo (igual que kitchen_orders_window)
        screen = QApplication.primaryScreen().geometry()
        self.is_small_screen = screen.width() <= 1366
        
        # Layout principal optimizado para resoluciones pequeñas (1366x768)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)  # Márgenes mínimos para laptop
        main_layout.setSpacing(4)  # Espaciado ultra-compacto
        
        # Header ultra-compacto
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Contenido principal en layout horizontal con espaciado mínimo
        content_layout = QHBoxLayout()
        content_layout.setSpacing(6)  # Espaciado mínimo
        
        # Panel izquierdo - Filtros (ancho más reducido)
        filters_panel = self.create_filters_panel()
        content_layout.addWidget(filters_panel)
        
        # Panel derecho - Tabla y controles (resto del espacio disponible)
        table_panel = self.create_table_panel()
        content_layout.addWidget(table_panel, 1)  # Factor de expansión
        
        main_layout.addLayout(content_layout)
        
        # Footer con controles de paginación y exportar
        footer_layout = self.create_footer_controls()
        main_layout.addLayout(footer_layout)
        
        # Estilo general mejorado (unificado con kitchen_orders_window)
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.PLATINUM},
                           stop:0.5 {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.98)},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)});
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }}
        """)
    
    def create_header(self):
        """Crear header simplificado usando el estilo de kitchen_orders_window"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        # Título simple y claro (mismo estilo que kitchen orders)
        title = QLabel("💰 HISTORIAL DE PAGOS")
        title_font_size = 22 if self.is_small_screen else 26
        title.setStyleSheet(f"""
            font-size: {title_font_size}px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            padding: 8px;
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Botones de acción unificados con kitchen_orders_window
        controls_container = QFrame()
        controls_container.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                border-radius: 8px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                padding: 8px;
            }}
        """)
        controls_layout = QHBoxLayout(controls_container)
        controls_layout.setSpacing(8)
        controls_layout.setContentsMargins(8, 6, 8, 6)
        
        # Tamaños responsivos
        screen = QApplication.primaryScreen().geometry()
        is_small_screen = screen.width() <= 1366
        btn_height = 34 if is_small_screen else 40
        btn_font_size = 12 if is_small_screen else 14
        
        # Botón volver a POS (estilo unificado)
        pos_btn = QPushButton("🍽️ Pos")
        pos_btn.setFixedHeight(btn_height)
        pos_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: white;
                border: none;
                padding: 6px;
                border-radius: 8px;
                font-weight: bold;
                font-size: {btn_font_size}px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        pos_btn.clicked.connect(lambda: self.back_to_pos.emit())
        controls_layout.addWidget(pos_btn)
        
        # Botón cocina (nuevo)
        kitchen_btn = QPushButton("👨‍🍳 Cocina")
        kitchen_btn.setFixedHeight(btn_height)
        kitchen_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.WARNING};
                color: white;
                border: none;
                padding: 6px;
                border-radius: 8px;
                font-weight: bold;
                font-size: {btn_font_size}px;
                min-width: 90px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)};
            }}
        """)
        kitchen_btn.clicked.connect(lambda: self.open_kitchen.emit())
        controls_layout.addWidget(kitchen_btn)
        
        layout.addWidget(controls_container)
        
        return layout
    
    def create_filters_panel(self):
        """Crear panel de filtros ultra-compacto para laptop 1366x768"""
        panel = QFrame()
        panel.setFixedWidth(200)  # Reducido aún más para laptop
        panel.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.PLATINUM},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)});
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                padding: 8px;
                margin: 1px;
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(6)  # Espaciado mínimo
        layout.setContentsMargins(6, 6, 6, 6)  # Márgenes mínimos
        
        # Título del panel más compacto
        title = QLabel("🔍 FILTROS")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            padding: 4px;
            background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
            border-radius: 4px;
            margin-bottom: 4px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Sección de fechas ultra-compacta
        date_section = QFrame()
        date_section.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.8)};
                border-radius: 6px;
                padding: 6px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        date_layout = QVBoxLayout(date_section)
        date_layout.setSpacing(4)  # Espaciado mínimo
        
        # Título de sección más compacto
        date_title = QLabel("📅 Fechas")
        date_title.setStyleSheet(f"""
            font-size: 15px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 2px;
        """)
        date_layout.addWidget(date_title)
        
        # Fecha desde
        from_label = QLabel("Desde:")
        from_label.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE}; font-weight: bold; font-size: 14px;")
        date_layout.addWidget(from_label)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        self.start_date.setFixedHeight(26)  # Aumentado +4 para laptop
        self.start_date.setStyleSheet(f"""
            QDateEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 3px;
                padding: 2px;
                font-size: 14px;
                color: {ColorPalette.RICH_BLACK};
            }}
            QDateEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
                background-color: white;
            }}
            QDateEdit::drop-down {{
                border: none;
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 2px;
                width: 16px;
            }}
        """)
        date_layout.addWidget(self.start_date)
        
        # Fecha hasta
        to_label = QLabel("Hasta:")
        to_label.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE}; font-weight: bold; font-size: 14px;")
        date_layout.addWidget(to_label)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setFixedHeight(26)  # Aumentado +4 para laptop
        self.end_date.setStyleSheet(f"""
            QDateEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 3px;
                padding: 2px;
                font-size: 14px;
                color: {ColorPalette.RICH_BLACK};
            }}
            QDateEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
                background-color: white;
            }}
            QDateEdit::drop-down {{
                border: none;
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 2px;
                width: 16px;
            }}
        """)
        date_layout.addWidget(self.end_date)
        
        layout.addWidget(date_section)
        
        # Sección de búsqueda compacta
        search_section = QFrame()
        search_section.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.8)};
                border-radius: 6px;
                padding: 6px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        search_layout = QVBoxLayout(search_section)
        search_layout.setSpacing(4)
        
        # Título de sección
        search_title = QLabel("🔎 Búsqueda")
        search_title.setStyleSheet(f"""
            font-size: 13px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 2px;
        """)
        search_layout.addWidget(search_title)
        
        search_label = QLabel("Orden/Cliente:")
        search_label.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE}; font-weight: bold; font-size: 12px;")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ej: #123 o Juan...")
        self.search_input.setFixedHeight(26)  # Aumentado +4 para laptop
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 3px;
                padding: 2px;
                font-size: 12px;
                color: {ColorPalette.RICH_BLACK};
            }}
            QLineEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
                background-color: white;
            }}
            QLineEdit::placeholder {{
                color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.7)};
                font-style: italic;
            }}
        """)
        self.search_input.returnPressed.connect(self.search_payments)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_section)
        
        # Botones de acción compactos
        buttons_section = QFrame()
        buttons_section.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border: none;
            }}
        """)
        buttons_layout = QVBoxLayout(buttons_section)
        buttons_layout.setSpacing(4)
        
        # Botón buscar compacto
        search_btn = QPushButton("🔍 BUSCAR")
        search_btn.setFixedHeight(28)  # Aumentado +4 para laptop
        search_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 {ColorPalette.YINMN_BLUE},
                           stop:1 {ColorPalette.OXFORD_BLUE});
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 4px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 {ColorPalette.OXFORD_BLUE},
                           stop:1 {ColorPalette.YINMN_BLUE});
            }}
        """)
        search_btn.clicked.connect(self.search_payments)
        buttons_layout.addWidget(search_btn)
        
        # Botón limpiar compacto
        clear_btn = QPushButton("🗑️ LIMPIAR")
        clear_btn.setFixedHeight(26)  # Aumentado +4 para laptop
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                color: {ColorPalette.RICH_BLACK};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                padding: 2px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        clear_btn.clicked.connect(self.clear_filters)
        buttons_layout.addWidget(clear_btn)
        
        layout.addWidget(buttons_section)
        
        # Espaciador al final
        layout.addStretch()
        
        return panel
    
    def create_table_panel(self):
        """Crear panel de tabla optimizado para laptop 1366x768"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.PLATINUM},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)});
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                padding: 6px;
                
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(6)  # Espaciado mínimo
        layout.setContentsMargins(8, 8, 8, 8)  # Márgenes mínimos
        
        # Header de la tabla más compacto
        table_header = QHBoxLayout()
        
        # Título principal más compacto
        table_title = QLabel("📋 TRANSACCIONES")
        table_title.setStyleSheet(f"""
            font-size: 18px;  # Aumentado +4 según nueva petición
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            padding: 2px;
        """)
        table_header.addWidget(table_title)
        
        table_header.addStretch()
        
        # Información de estado/carga más compacta
        self.table_status = QLabel("Datos actualizados")
        self.table_status.setStyleSheet(f"""
            color: {ColorPalette.SUCCESS};
            font-size: 13px;  # Aumentado +4 según nueva petición
            font-weight: bold;
            padding: 2px;
            background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.1)};
            border-radius: 3px;  # Muy reducido
            border: 1px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.3)};
        """)
        table_header.addWidget(self.table_status)
        
        # Botón exportar más compacto
        export_btn = QPushButton("📤 Excel")
        export_btn.setFixedSize(75, 28)  # Aumentado para acomodar texto más grande
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 2px 4px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;  # Aumentado +4 según nueva petición
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        export_btn.clicked.connect(self.export_data)
        table_header.addWidget(export_btn)
        
        layout.addLayout(table_header)
        
        # Crear tabla con diseño compacto y bien dimensionado
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(6)  # 6 columnas optimizadas
        self.payment_table.setHorizontalHeaderLabels([
            "Fecha", "Orden", "Cliente", "Total", "Método", "Ver"
        ])
        
        # Configurar tabla con proporciones exactas para laptop 1366x768
        header = self.payment_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)          # Fecha - ancho fijo
        header.setSectionResizeMode(1, QHeaderView.Fixed)          # Orden - ancho fijo
        header.setSectionResizeMode(2, QHeaderView.Stretch)        # Cliente - expandible
        header.setSectionResizeMode(3, QHeaderView.Fixed)          # Total - ancho fijo
        header.setSectionResizeMode(4, QHeaderView.Fixed)          # Método - ancho fijo
        header.setSectionResizeMode(5, QHeaderView.Fixed)          # Acción - ancho fijo
        
        # Establecer anchos específicos calculados para evitar solapamiento
        self.payment_table.setColumnWidth(0, 90)   # Fecha - espacio justo para dd/mm/yyyy
        self.payment_table.setColumnWidth(1, 55)   # Orden - espacio para #123
        # Cliente: se expande automáticamente (resto del espacio)
        self.payment_table.setColumnWidth(3, 200)   # Total - espacio para $999.99
        self.payment_table.setColumnWidth(4, 150)   # Método - espacio para "Efec." o "Tarj."
        self.payment_table.setColumnWidth(5, 45)   # Acción - botón pequeño
        
        # Configuración adicional de la tabla
        self.payment_table.setAlternatingRowColors(True)
        self.payment_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.payment_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.payment_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.payment_table.setSortingEnabled(True)
        self.payment_table.setGridStyle(Qt.SolidLine)
        
        # Filas con altura adecuada para mostrar todo el texto
        self.payment_table.verticalHeader().setDefaultSectionSize(30)  # Altura aumentada +2
        self.payment_table.verticalHeader().setVisible(False)  # Ocultar números de fila para ahorrar espacio
        
        # Estilo mejorado de la tabla para laptop con espaciado correcto
        self.payment_table.setStyleSheet(f"""
            QTableWidget {{
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                background-color: {ColorPalette.PLATINUM};
                gridline-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                selection-background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
                font-size: 13px;  /* Aumentado +4 según nueva petición */
            }}
            QTableWidget::item {{
                padding: 3px 2px;  /* Padding aumentado para mejor legibilidad */
                border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                color: {ColorPalette.RICH_BLACK};
            }}
            QTableWidget::item:selected {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
                color: {ColorPalette.RICH_BLACK};
            }}
            QTableWidget::item:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.YINMN_BLUE},
                           stop:1 {ColorPalette.OXFORD_BLUE});
                color: {ColorPalette.PLATINUM};
                padding: 6px 4px;  /* Padding aumentado para mostrar texto completo */
                font-weight: bold;
                font-size: 12px;  /* Aumentado +4 según nueva petición */
                border: none;
                border-right: 1px solid {ColorPalette.OXFORD_BLUE};
                height: 36px;  /* Altura aumentada para acomodar texto más grande */
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 6px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 6px;
                border-right: none;
            }}
            QScrollBar:vertical {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                width: 8px;  /* Scrollbar muy delgado */
                border-radius: 4px;
                
            }}
            QScrollBar::handle:vertical {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        
        layout.addWidget(self.payment_table)
        
        return panel
    
    def create_footer_controls(self):
        """Crear controles de footer ultra-compactos para laptop 1366x768"""
        layout = QHBoxLayout()
        layout.setContentsMargins(4, 2, 4, 2)  # Márgenes mínimos para laptop
        layout.setSpacing(6)  # Espaciado muy reducido
        
        # Panel izquierdo - Información de registros ultra-compacto
        info_panel = QFrame()
        info_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 4px;
                padding: 2px;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
            }}
        """)
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(3, 1, 3, 1)
        
        # Ícono de información muy pequeño
        info_icon = QLabel("📊")
        info_icon.setStyleSheet("font-size: 10px; padding-right: 1px;")
        info_layout.addWidget(info_icon)
        
        # Información de paginación muy compacta
        self.pagination_info = QLabel("Mostrando 0 de 0")
        self.pagination_info.setStyleSheet(f"""
            color: {ColorPalette.RICH_BLACK};
            font-weight: bold;
            font-size: 9px;
        """)
        info_layout.addWidget(self.pagination_info)
        
        layout.addWidget(info_panel)
        
        layout.addStretch()
        
        # Panel central - Controles de paginación ultra-compactos
        pagination_panel = QFrame()
        pagination_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
                border-radius: 4px;
                padding: 2px 4px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
            }}
        """)
        pagination_layout = QHBoxLayout(pagination_panel)
        pagination_layout.setSpacing(3)  # Espaciado muy reducido
        pagination_layout.setContentsMargins(3, 1, 3, 1)  # Márgenes muy reducidos
        
        # Botón página anterior muy pequeño
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(20, 20)  # Muy pequeño para laptop
        self.prev_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 2px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 8px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.5)};
                color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.7)};
            }}
        """)
        self.prev_btn.setToolTip("Página anterior")
        self.prev_btn.clicked.connect(self.previous_page)
        pagination_layout.addWidget(self.prev_btn)
        
        # Información de página actual muy compacta
        self.page_info = QLabel("1/1")
        self.page_info.setStyleSheet(f"""
            color: {ColorPalette.RICH_BLACK};
            font-weight: bold;
            font-size: 9px;
            padding: 2px 4px;
            background-color: {ColorPalette.PLATINUM};
            border-radius: 3px;
            border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
        """)
        self.page_info.setAlignment(Qt.AlignCenter)
        self.page_info.setMinimumWidth(30)  # Muy reducido
        pagination_layout.addWidget(self.page_info)
        
        # Botón página siguiente muy pequeño
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(20, 20)  # Muy pequeño para laptop
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 2px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 8px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.5)};
                color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.7)};
            }}
        """)
        self.next_btn.setToolTip("Página siguiente")
        self.next_btn.clicked.connect(self.next_page)
        pagination_layout.addWidget(self.next_btn)
        
        layout.addWidget(pagination_panel)
        
        layout.addStretch()
        
        # Panel derecho - Acciones adicionales muy compacto
        actions_panel = QFrame()
        actions_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 4px;
                padding: 2px 4px;
                border: 1px solid {ColorPalette.SUCCESS};
            }}
        """)
        actions_layout = QHBoxLayout(actions_panel)
        actions_layout.setContentsMargins(3, 1, 3, 1)
        actions_layout.setSpacing(2)
        
        # Indicador de estado muy pequeño
        status_icon = QLabel("✅")
        status_icon.setStyleSheet("font-size: 8px;")
        actions_layout.addWidget(status_icon)
        
        status_text = QLabel("OK")
        status_text.setStyleSheet(f"""
            color: {ColorPalette.SUCCESS};
            font-weight: bold;
            font-size: 8px;
        """)
        actions_layout.addWidget(status_text)
        
        layout.addWidget(actions_panel)
        
        return layout
    
    def load_payment_history(self):
        """Cargar historial de pagos con indicadores visuales mejorados"""
        # Mostrar estado de carga compacto
        self.table_status.setText("🔄")
        self.table_status.setStyleSheet(f"""
            color: {ColorPalette.WARNING};
            font-size: 13px;  # Aumentado +4 según nueva petición
            font-weight: bold;
            padding: 2px 4px;
            background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.1)};
            border-radius: 3px;
            border: 1px solid {ColorPalette.with_alpha(ColorPalette.WARNING, 0.3)};
        """)
        self.pagination_info.setText("Cargando...")
        
        # Obtener valores de filtros
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        search_term = self.search_input.text().strip() or None
        
        try:
            # Obtener datos
            result = self.payment_controller.get_payment_history(
                start_date=start_date,
                end_date=end_date,
                search_term=search_term,
                page=self.current_page,
                page_size=self.page_size
            )
            
            self.current_orders = result['orders']
            
            # Actualizar tabla
            self.update_table(result['orders'])
            
            # Actualizar información de paginación
            self.update_pagination_info(result)
            
        # Actualizar estado de éxito con formato compacto
            self.table_status.setText("✅ OK")
            self.table_status.setStyleSheet(f"""
                color: {ColorPalette.SUCCESS};
                font-size: 13px;  # Aumentado +4 según nueva petición
                font-weight: bold;
                padding: 2px 4px;  # Mínimo padding
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.1)};
                border-radius: 3px;  # Muy reducido
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.3)};
            """)
            
        except Exception as e:
            # Mostrar estado de error compacto
            self.table_status.setText("❌")
            self.table_status.setStyleSheet(f"""
                color: {ColorPalette.ERROR};
                font-size: 13px;  # Aumentado +4 según nueva petición
                font-weight: bold;
                padding: 2px 4px;
                background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.1)};
                border-radius: 3px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.ERROR, 0.3)};
            """)
            self.pagination_info.setText(f"Error: {str(e)}")
            print(f"Error cargando historial: {e}")
    
    def update_table(self, orders):
        """Actualizar contenido de la tabla con diseño optimizado para laptop sin solapamiento"""
        self.payment_table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            # Fecha compacta (solo fecha, formato corto)
            date_str = order.created_at.strftime('%d/%m/%y')  # Formato más corto
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setFont(QFont("Arial", 11))  # Aumentado +4 según nueva petición
            self.payment_table.setItem(row, 0, date_item)
            
            # Orden # compacto
            order_item = QTableWidgetItem(f"#{order.id}")
            order_item.setTextAlignment(Qt.AlignCenter)
            order_item.setFont(QFont("Arial", 11, QFont.Bold))  # Aumentado +4 según nueva petición
            order_item.setForeground(QColor(ColorPalette.YINMN_BLUE))
            self.payment_table.setItem(row, 1, order_item)
            
            # Cliente - truncar si es muy largo para evitar solapamiento
            customer_name = order.customer_name
            if len(customer_name) > 15:  # Truncar nombres largos
                customer_name = customer_name[:12] + "..."
            customer_item = QTableWidgetItem(customer_name)
            customer_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            customer_item.setFont(QFont("Arial", 11))  # Aumentado +4 según nueva petición
            customer_item.setToolTip(order.customer_name)  # Tooltip con nombre completo
            self.payment_table.setItem(row, 2, customer_item)
            
            # Total con formato compacto
            total_item = QTableWidgetItem(f"$ {order.total:,.0f}")  # Sin decimales para ahorrar espacio
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            total_item.setFont(QFont("Arial", 11, QFont.Bold))  # Aumentado +4 según nueva petición
            total_item.setForeground(QColor(ColorPalette.SUCCESS))
            total_item.setToolTip(f"${order.total:,.0f}")  # Tooltip con decimales
            self.payment_table.setItem(row, 3, total_item)
            
            # Método de pago muy abreviado
            method = (order.payment_method or 'Efectivo')
            if method.lower() == 'efectivo':
                method = 'Efec'
            elif method.lower() == 'tarjeta':
                method = 'Tarj'
            elif method.lower() == 'transferencia':
                method = 'Transf'
            else:
                method = method[:5]  # Máximo 5 caracteres
            
            method_item = QTableWidgetItem(method)
            method_item.setTextAlignment(Qt.AlignCenter)
            method_item.setFont(QFont("Arial", 11))  # Aumentado +4 según nueva petición
            method_item.setToolTip(order.payment_method or 'Efectivo')  # Tooltip completo
            self.payment_table.setItem(row, 4, method_item)
            
            # Botón de acción muy compacto sin texto
            action_btn = QPushButton("👁")
            action_btn.setFixedSize(24, 24)  # Aumentado +4 para acomodar texto más grande
            action_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.YINMN_BLUE};
                    color: {ColorPalette.PLATINUM};
                    border: none;
                    border-radius: 2px;
                    font-size: 11px;  # Aumentado +4 según nueva petición
                    font-weight: bold;
                    
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.OXFORD_BLUE};
                }}
            """)
            action_btn.setToolTip(f"Ver detalles de la orden #{order.id}")
            action_btn.clicked.connect(lambda checked, o=order: self.show_order_details(o))
            self.payment_table.setCellWidget(row, 5, action_btn)
            
            # Establecer altura de fila para mostrar todo el contenido
            self.payment_table.setRowHeight(row, 30)  # Altura aumentada +2
    
    def update_pagination_info(self, result):
        """Actualizar información de paginación con formato compacto"""
        total_orders = result.get('total', 0)
        current_page = result.get('current_page', 1)
        total_pages = result.get('total_pages', 1)
        
        # Calcular rango de registros mostrados
        start_record = (current_page - 1) * self.page_size + 1
        end_record = min(current_page * self.page_size, total_orders)
        
        # Actualizar información con formato muy compacto
        self.pagination_info.setText(f"{start_record}-{end_record} de {total_orders}")
        self.page_info.setText(f"{current_page}/{total_pages}")
        
        # Habilitar/deshabilitar botones
        self.prev_btn.setEnabled(current_page > 1)
        self.next_btn.setEnabled(current_page < total_pages)
    
    def search_payments(self):
        """Buscar pagos con filtros actuales"""
        # Refrescar controlador para obtener datos más recientes
        self.payment_controller = PaymentController()
        self.current_page = 1  # Resetear a primera página
        self.load_payment_history()
    
    def clear_filters(self):
        """Limpiar filtros"""
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.end_date.setDate(QDate.currentDate())
        self.search_input.clear()
        self.search_payments()
    
    def previous_page(self):
        """Ir a página anterior"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_payment_history()
    
    def next_page(self):
        """Ir a página siguiente"""
        self.current_page += 1
        self.load_payment_history()
    
    def show_order_details(self, order):
        """Mostrar detalles de una orden"""
        dialog = PaymentDetailDialog(order, self)
        dialog.exec_()
    
    def export_data(self):
        """Exportar datos actuales a Excel"""
        if not self.current_orders:
            QMessageBox.warning(self, "Sin Datos", "No hay datos para exportar")
            return
        
        # Seleccionar ubicación del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"historial_pagos_{timestamp}.xlsx"
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Historial de Pagos",
            default_filename,
            "Excel files (*.xlsx);;All files (*.*)"
        )
        
        if filename:
            # Crear y mostrar progress bar
            progress = QProgressBar(self)
            progress.setRange(0, 0)  # Modo indeterminado
            progress.show()
            
            # Preparar datos serializados para evitar problemas de thread
            serialized_data = []
            for order in self.current_orders:
                # Acceder a todas las relaciones en el hilo principal
                order_data = {
                    'id': order.id,
                    'created_at': order.created_at,
                    'customer_name': order.customer_name,
                    'table_number': order.table_number,
                    'status': order.status,
                    'status_display': order.status_display,
                    'total': order.total,
                    'payment_method': order.payment_method,
                    'items': []
                }
                
                # Cargar items y productos en el hilo principal
                for item in order.items:
                    item_data = {
                        'quantity': item.quantity,
                        'unit_price': item.unit_price,
                        'subtotal': item.subtotal,
                        'product_name': item.product.name
                    }
                    order_data['items'].append(item_data)
                
                serialized_data.append(order_data)
            
            # Crear thread para exportar con datos serializados
            self.export_thread = ExportThread(
                serialized_data,
                filename  # Usar la ruta completa seleccionada por el usuario
            )
            self.export_thread.finished.connect(lambda path: self.export_finished(path, progress))
            self.export_thread.error.connect(lambda err: self.export_error(err, progress))
            self.export_thread.start()
    
    @pyqtSlot(str)
    def export_finished(self, filepath, progress):
        """Callback cuando termina la exportación"""
        progress.hide()
        QMessageBox.information(
            self,
            "Exportación Exitosa",
            f"Archivo guardado en:\n{filepath}"
        )
    
    @pyqtSlot(str)
    def export_error(self, error_msg, progress):
        """Callback cuando hay error en la exportación"""
        progress.hide()
        QMessageBox.critical(
            self,
            "Error de Exportación",
            f"Error al exportar datos:\n{error_msg}"
        )
