# views/pos_window.py
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QPushButton, QFrame, QGridLayout, QScrollArea,
                             QComboBox, QApplication, QDialog, QFormLayout, QLineEdit,
                             QSpinBox, QStackedWidget, QMessageBox, QSizePolicy)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from utils.printer import ReceiptPrinter
from utils.colors import ColorPalette, CommonStyles

class ModernButton(QPushButton):
    """Botón personalizado con efectos hover"""
    def __init__(self, text, style_type="primary"):
        super().__init__(text)
        self.style_type = style_type
        self.setStyleSheet(self.get_style())
    
    def get_style(self):
        if self.style_type == "primary":
            return CommonStyles.button_primary()
        elif self.style_type == "secondary":
            return CommonStyles.button_secondary()
        elif self.style_type == "success":
            return CommonStyles.button_success()
        elif self.style_type == "warning":
            return CommonStyles.button_warning()
        elif self.style_type == "danger":
            return CommonStyles.button_danger()
        else:
            return CommonStyles.button_primary()

class CartItemWidget(QWidget):
    """Widget personalizado para items del carrito"""
    
    quantity_changed = pyqtSignal(int, int)  # product_id, new_quantity
    item_removed = pyqtSignal(int)  # product_id
    
    def __init__(self, product, quantity):
        super().__init__()
        self.product = product
        self.quantity = quantity
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)  # Cambiar a vertical para mejor uso del espacio
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)
        
        # Primera fila: Nombre del producto
        name_label = QLabel(self.product.name)
        name_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.RICH_BLACK}; font-size: 11px;")
        name_label.setWordWrap(True)
        name_label.setMaximumHeight(30)  # Limitar altura para evitar que ocupe mucho espacio
        layout.addWidget(name_label)
        
        # Segunda fila: Controles (cantidad, precio, eliminar)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(6)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Controles de cantidad más compactos
        qty_layout = QHBoxLayout()
        qty_layout.setSpacing(4)
        
        minus_btn = QPushButton("-")
        minus_btn.setFixedSize(22, 22)
        minus_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 11px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)}; }}
        """)
        minus_btn.clicked.connect(self.decrease_quantity)
        qty_layout.addWidget(minus_btn)
        
        self.qty_label = QLabel(str(self.quantity))
        self.qty_label.setAlignment(Qt.AlignCenter)
        self.qty_label.setFixedWidth(25)
        self.qty_label.setStyleSheet(f"font-weight: bold; font-size: 12px; color: {ColorPalette.RICH_BLACK};")
        qty_layout.addWidget(self.qty_label)
        
        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(22, 22)
        plus_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 11px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)}; }}
        """)
        plus_btn.clicked.connect(self.increase_quantity)
        qty_layout.addWidget(plus_btn)
        
        controls_layout.addLayout(qty_layout)
        
        # Espaciador flexible
        controls_layout.addStretch()
        
        # Precio
        self.price_label = QLabel(f"$ {self.product.price * self.quantity:,.0f}")
        self.price_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.SUCCESS}; font-size: 11px;")
        self.price_label.setFixedWidth(55)
        self.price_label.setAlignment(Qt.AlignCenter)
        controls_layout.addWidget(self.price_label)
        
        # Botón eliminar más visible
        remove_btn = QPushButton("🗑️")
        remove_btn.setFixedSize(28, 22)
        remove_btn.setToolTip("Eliminar del carrito")
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{ 
                background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
                border: 2px solid {ColorPalette.PLATINUM};
            }}
        """)
        remove_btn.clicked.connect(lambda: self.item_removed.emit(self.product.id))
        controls_layout.addWidget(remove_btn)
        
        layout.addLayout(controls_layout)
        
        # Estilo del widget - más compacto para layout vertical
        self.setStyleSheet(f"""
            CartItemWidget {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 8px;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                min-height: 55px;
                max-height: 65px;
            }}
            CartItemWidget:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                border: 1px solid {ColorPalette.YINMN_BLUE};
            }}
        """)
    
    def increase_quantity(self):
        self.quantity += 1
        self.qty_label.setText(str(self.quantity))
        self.price_label.setText(f"$ {self.product.price * self.quantity:,.0f}")
        self.quantity_changed.emit(self.product.id, self.quantity)
    
    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.qty_label.setText(str(self.quantity))
            self.price_label.setText(f"$ {self.product.price * self.quantity:,.0f}")
            self.quantity_changed.emit(self.product.id, self.quantity)

class CustomerInfoDialog(QDialog):
    """Dialog para capturar información del cliente y método de pago"""
    
    def __init__(self, total_amount, parent=None, payment_required=True):
        super().__init__(parent)
        self.total_amount = total_amount
        self.payment_required = payment_required
        self.setWindowTitle("Información del Pedido" if not payment_required else "Información del Pedido y Pago")
        self.setFixedSize(380, 420 if payment_required else 320)  # Tamaño más pequeño sin pago
        self.setModal(True)
        self.payment_method = "efectivo"
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título más pequeño
        title = QLabel("Información del Pedido")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 16px; 
            font-weight: bold; 
            color: {ColorPalette.RICH_BLACK};
            padding: 5px;
        """)
        layout.addWidget(title)
        
        # Total compacto
        total_frame = QFrame()
        total_frame.setFixedHeight(40)
        total_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                           stop:0 {ColorPalette.YINMN_BLUE}, 
                           stop:1 {ColorPalette.OXFORD_BLUE});
                border-radius: 8px;
            }}
        """)
        total_layout = QVBoxLayout(total_frame)
        total_layout.setContentsMargins(10, 8, 10, 8)
        
        total_label = QLabel(f"Total: ${self.total_amount:,.0f}")
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet(f"""
            color: {ColorPalette.PLATINUM}; 
            font-size: 16px; 
            font-weight: bold;
        """)
        total_layout.addWidget(total_label)
        layout.addWidget(total_frame)
        
        # Cliente compacto
        name_label = QLabel("Cliente:")
        name_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.RICH_BLACK}; font-size: 13px;")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del cliente")
        self.name_input.setText("Cliente")
        self.name_input.setFixedHeight(28)
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 5px;
                padding: 5px 8px;
                font-size: 13px;
                color: {ColorPalette.RICH_BLACK};
            }}
            QLineEdit:focus {{
                border: 1px solid {ColorPalette.YINMN_BLUE};
            }}
        """)
        layout.addWidget(self.name_input)
        
        # Mesa compacto
        table_label = QLabel("Mesa:")
        table_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.RICH_BLACK}; font-size: 13px;")
        layout.addWidget(table_label)
        
        self.table_input = QSpinBox()
        self.table_input.setRange(0, 99)
        self.table_input.setValue(0)
        self.table_input.setSpecialValueText("Para llevar")
        self.table_input.setFixedHeight(28)
        self.table_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 5px;
                padding: 5px 8px;
                font-size: 13px;
                color: {ColorPalette.RICH_BLACK};
            }}
            QSpinBox:focus {{
                border: 1px solid {ColorPalette.YINMN_BLUE};
            }}
        """)
        layout.addWidget(self.table_input)
        
        # Método de pago compacto (solo si se requiere pago)
        if self.payment_required:
            payment_title = QLabel("Método de Pago:")
            payment_title.setStyleSheet(f"""
                font-weight: bold; 
                color: {ColorPalette.RICH_BLACK}; 
                font-size: 13px;
                padding: 5px 0px 0px 0px;
            """)
            layout.addWidget(payment_title)
            
            # Botones de método de pago más pequeños
            payment_buttons_layout = QHBoxLayout()
            payment_buttons_layout.setSpacing(8)
            
            self.cash_btn = QPushButton("💵\nEfectivo")
            self.transfer_btn = QPushButton("🏦\nTransf.")
            self.card_btn = QPushButton("💳\nTarjeta")
            
            # Configurar botones más pequeños
            for btn in [self.cash_btn, self.transfer_btn, self.card_btn]:
                btn.setCheckable(True)
                btn.setFixedSize(70, 45)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {ColorPalette.PLATINUM};
                        color: {ColorPalette.RICH_BLACK};
                        border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                        padding: 3px;
                        border-radius: 5px;
                        font-weight: bold;
                        font-size: 10px;
                    }}
                    QPushButton:checked {{
                        background-color: {ColorPalette.YINMN_BLUE};
                        color: {ColorPalette.PLATINUM};
                        border: 1px solid {ColorPalette.OXFORD_BLUE};
                    }}
                    QPushButton:hover {{
                        border: 1px solid {ColorPalette.YINMN_BLUE};
                    }}
                """)
            
            # Conectar eventos
            self.cash_btn.clicked.connect(lambda: self.set_payment_method("efectivo"))
            self.transfer_btn.clicked.connect(lambda: self.set_payment_method("transferencia"))
            self.card_btn.clicked.connect(lambda: self.set_payment_method("tarjeta"))
            
            # Establecer efectivo como seleccionado por defecto
            self.cash_btn.setChecked(True)
            
            payment_buttons_layout.addWidget(self.cash_btn)
            payment_buttons_layout.addWidget(self.transfer_btn)
            payment_buttons_layout.addWidget(self.card_btn)
            payment_buttons_layout.addStretch()
            
            layout.addLayout(payment_buttons_layout)
        
        # Espaciador pequeño
        layout.addSpacing(10)
        
        # Botones de acción más pequeños
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setFixedHeight(35)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("✅ Procesar Pedido")
        ok_btn.setFixedHeight(35)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        ok_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_btn)
        
        layout.addLayout(buttons_layout)
        
        # Estilo general del diálogo
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {ColorPalette.PLATINUM};
            }}
        """)
    
    def set_payment_method(self, method):
        """Establecer método de pago y actualizar botones"""
        self.payment_method = method
        
        # Desmarcar todos los botones
        self.cash_btn.setChecked(False)
        self.transfer_btn.setChecked(False)
    def set_payment_method(self, method):
        """Establecer método de pago seleccionado"""
        if not self.payment_required:
            return
            
        self.payment_method = method
        
        # Desmarcar todos los botones
        self.cash_btn.setChecked(False)
        self.transfer_btn.setChecked(False)
        self.card_btn.setChecked(False)
        
        # Marcar el botón seleccionado
        if method == "efectivo":
            self.cash_btn.setChecked(True)
        elif method == "transferencia":
            self.transfer_btn.setChecked(True)
        elif method == "tarjeta":
            self.card_btn.setChecked(True)
    
    def get_customer_info(self):
        """Retorna la información del cliente y método de pago"""
        info = {
            'name': self.name_input.text().strip() or "Cliente",
            'table': self.table_input.value() if self.table_input.value() > 0 else None,
        }
        
        # Solo incluir método de pago si se requiere
        if self.payment_required:
            info['payment_method'] = self.payment_method
        
        return info

class POSWindow(QMainWindow):
    """Ventana POS mejorada con diseño moderno"""
    
    # Señales para comunicación con el controlador principal
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.product_controller = ProductController()
        self.order_controller = OrderController()
        self.printer = ReceiptPrinter()
        self.cart_items = {}  # Cambiar a dict para mejor manejo
        
        # Stack widget para manejar las vistas
        self.stack_widget = QStackedWidget()
        self.setCentralWidget(self.stack_widget)
        
        # Crear vistas
        self.pos_view = QWidget()
        self.kitchen_view = None  # Se creará cuando se necesite
        self.payment_history_view = None  # Se creará cuando se necesite
        
        self.init_ui()
        self.load_categories()
        
        # Agregar vista POS al stack
        self.stack_widget.addWidget(self.pos_view)
        
    def init_ui(self):
        self.setWindowTitle("🍔 POS - Restaurante FastFood")
        
        # Detectar resolución para diseño responsivo
        screen = QApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        self.is_small_screen = self.screen_width <= 1366
        
        print(f"🖥️ Resolución detectada: {self.screen_width}x{self.screen_height}")
        print(f"📱 Pantalla pequeña: {self.is_small_screen}")
        
        # Configurar ventana para permitir maximización correcta
        if self.screen_width <= 1366:
            # Para resolución 1366x768 - configurar para portátil
            self.setMinimumSize(800, 500)
            # NO auto-maximizar, permitir que el usuario lo haga manualmente
            self.resize(1100, 650)  # Tamaño inicial razonable
        else:
            # Para pantallas más grandes
            self.setMinimumSize(1200, 700)
            available_width = min(self.screen_width - 100, 1400)
            available_height = min(self.screen_height - 100, 800)
            self.resize(available_width, available_height)
            
            # Centrar la ventana en la pantalla
            screen_center = screen.center()
            window_rect = self.frameGeometry()
            window_rect.moveCenter(screen_center)
            self.move(window_rect.topLeft())
        
        # Layout principal para la vista POS con espaciado adaptativo
        main_layout = QHBoxLayout(self.pos_view)
        spacing = 5 if self.is_small_screen else 15
        margins = 5 if self.is_small_screen else 15
        main_layout.setSpacing(spacing)
        main_layout.setContentsMargins(margins, margins, margins, margins)
        
        # Ajustar proporciones según pantalla - siempre usar proporción 75/25
        left_panel = self.create_product_panel()
        main_layout.addWidget(left_panel, 75)
        
        right_panel = self.create_cart_panel()
        main_layout.addWidget(right_panel, 25)
        
        # Estilo general
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {ColorPalette.gradient_background()};
            }}
        """)
    
    def create_product_panel(self):
        panel = QFrame()
        panel.setStyleSheet(CommonStyles.panel_main())
        layout = QVBoxLayout(panel)
        
        # Espaciado adaptativo
        spacing = 10 if self.is_small_screen else 15
        layout.setSpacing(spacing)
        
        # Header del panel
        header_layout = QHBoxLayout()
        
        # Contenedor del título con gradiente de fondo (estilo unificado con kitchen_orders)
        title_container = QFrame()
        title_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.PLATINUM},
                           stop:0.5 {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.98)},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)});
                border-radius: 8px;
                padding: 8px 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
            }}
        """)
        title_container_layout = QHBoxLayout(title_container)
        title_container_layout.setContentsMargins(4, 2, 4, 2)
        
        title = QLabel("🍽️ MENÚ")
        title.setAlignment(Qt.AlignLeft)
        title_font_size = 22 if self.is_small_screen else 26
        title.setStyleSheet(f"""
            font-size: {title_font_size}px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            background: transparent;
            border: none;
            padding: 4px 8px;
        """)
        title_container_layout.addWidget(title)
        title_container_layout.addStretch()
        
        header_layout.addWidget(title_container)
        
        header_layout.addStretch()
        
        # Botón abrir cocina (estilo unificado)
        kitchen_btn = QPushButton("👨‍🍳 Cocina")
        kitchen_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.WARNING};
                color: #ffffff;
                border: none;
                padding: 12px 18px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)};
            }}
        """)
        kitchen_btn.clicked.connect(self.open_kitchen_window)
        header_layout.addWidget(kitchen_btn)
        
        # Botón historial de pagos (estilo unificado)
        history_btn = QPushButton("💰 Historial")
        history_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: #ffffff;
                border: none;
                padding: 12px 18px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        history_btn.clicked.connect(self.open_payment_history)
        header_layout.addWidget(history_btn)
        
        # Botón cerrar sesión
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.ERROR};
                color: #ffffff;
                border: none;
                padding: 12px 18px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
            }}
        """)
        logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(logout_btn)
        
        layout.addLayout(header_layout)
        
        # Área de categorías con scroll horizontal
        categories_scroll = QScrollArea()
        categories_scroll.setWidgetResizable(True)
        categories_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        categories_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        categories_scroll.setFixedHeight(70)  # Altura fija para el área de categorías
        categories_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:horizontal {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                height: 8px;
                border-radius: 4px;
                margin: 2px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 4px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
            }}
        """)
        
        # Widget contenedor para los botones de categorías
        categories_frame = QFrame()
        categories_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                border-radius: 12px;
                padding: 10px;
                min-height: 50px;
            }}
        """)
        categories_layout = QHBoxLayout(categories_frame)
        categories_layout.setSpacing(8)
        categories_layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear botones de categorías
        self.category_buttons = []
        self.selected_category_id = None
        
        # Botón "Todas"
        all_btn = QPushButton("🍽️ Todas")
        all_btn.setCheckable(True)
        all_btn.setChecked(True)  # Por defecto seleccionado
        all_btn.setMinimumWidth(100)  # Ancho mínimo para evitar botones muy pequeños
        all_btn.setFixedHeight(40)   # Altura fija para consistencia
        
        # Estilo inicial para el botón "Todas"
        all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: 2px solid {ColorPalette.OXFORD_BLUE};
                padding: 10px 16px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
                height: 40px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        
        all_btn.clicked.connect(lambda: self.select_category(None, all_btn))
        self.category_buttons.append(all_btn)
        categories_layout.addWidget(all_btn)
        
        # Configurar el scroll area
        categories_scroll.setWidget(categories_frame)
        layout.addWidget(categories_scroll)
        
        # Área de productos con scroll mejorado
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        
        self.products_widget = QWidget()
        self.products_layout = QGridLayout(self.products_widget)
        
        # Espaciado optimizado para 1366x768
        if self.screen_width <= 1366:
            spacing = 10  # Espaciado óptimo para 4 columnas
            margin = 10   # Márgenes ajustados
        else:
            spacing = 12  # Espaciado estándar para pantallas más grandes
            margin = 15
        
        self.products_layout.setSpacing(spacing)
        self.products_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.products_layout.setContentsMargins(margin, margin, margin, margin)
        
        scroll.setWidget(self.products_widget)
        layout.addWidget(scroll)
        
        return panel
    
    def create_cart_panel(self):
        panel = QFrame()
        panel.setStyleSheet(CommonStyles.panel_main())
        
        # Configuración de ancho del carrito optimizada - usar ancho dinámico
        current_width = self.width()
        if current_width > 0:
            # Calcular 25% del ancho total
            cart_width = max(250, min(400, int(current_width * 0.25)))
        else:
            # Valores por defecto si no tenemos ancho aún
            cart_width = 280 if self.is_small_screen else 350
            
        panel.setMaximumWidth(cart_width)
        panel.setMinimumWidth(max(250, cart_width - 50))  # Mínimo más flexible
        
        layout = QVBoxLayout(panel)
        spacing = 6 if self.is_small_screen else 15
        layout.setSpacing(spacing)
        layout.setContentsMargins(8, 8, 8, 8)  # Márgenes más pequeños
        
        print(f"🛒 Carrito configurado: ancho={cart_width}, ventana={current_width}")
        
        # Header del carrito mejorado y más compacto
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: {ColorPalette.gradient_primary()};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(3)  # Espaciado reducido
        
        title = QLabel("🛒 ORDEN")  # Título más corto
        title.setAlignment(Qt.AlignCenter)
        title_font_size = 16 if self.screen_width <= 1366 else 18  # Fuente más pequeña
        title.setStyleSheet(f"""
            font-size: {title_font_size}px;
            font-weight: bold;
            color: {ColorPalette.PLATINUM};
            padding: 0px;
        """)
        header_layout.addWidget(title)
        
        # Contador de items en el header
        self.items_count_label = QLabel("0 productos")
        self.items_count_label.setAlignment(Qt.AlignCenter)
        count_font_size = 12 if self.screen_width <= 1366 else 14
        self.items_count_label.setStyleSheet(f"color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.9)}; font-size: {count_font_size}px; font-weight: bold;")
        header_layout.addWidget(self.items_count_label)
        
        layout.addWidget(header_frame)
        
        # Scroll area para items del carrito con mejor estilo
        cart_scroll = QScrollArea()
        cart_scroll.setWidgetResizable(True)
        cart_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        cart_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        cart_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)};
                border-radius: 8px;
            }}
            QScrollBar:vertical {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                width: 6px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 3px;
                min-height: 15px;
            }}
        """)
        
        self.cart_container = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container)
        self.cart_layout.setAlignment(Qt.AlignTop)
        self.cart_layout.setSpacing(4)  # Espaciado reducido
        self.cart_layout.setContentsMargins(3, 3, 3, 3)  # Márgenes reducidos
        
        cart_scroll.setWidget(self.cart_container)
        layout.addWidget(cart_scroll)
        
        # Resumen del total con diseño más compacto
        total_frame = QFrame()
        total_frame.setStyleSheet(f"""
            QFrame {{
                background: {ColorPalette.gradient_secondary()};
                border-radius: 12px;
                padding: 15px;
                border: 1px solid {ColorPalette.OXFORD_BLUE};
            }}
        """)
        total_layout = QVBoxLayout(total_frame)
        
        self.total_label = QLabel("Total: $0")
        self.total_label.setAlignment(Qt.AlignCenter)
        total_font_size = 20 if self.screen_width <= 1366 else 26  # Fuente más pequeña
        self.total_label.setStyleSheet(f"color: {ColorPalette.PLATINUM}; font-size: {total_font_size}px; font-weight: bold;")
        total_layout.addWidget(self.total_label)
        
        layout.addWidget(total_frame)
        
        # Botones de acción con espaciado optimizado
        buttons_layout = QVBoxLayout()
        button_spacing = 8 if self.screen_width <= 1366 else 12
        buttons_layout.setSpacing(button_spacing)
        
        # Botón limpiar carrito más compacto
        clear_btn = QPushButton("🗑️ Limpiar")  # Texto más corto
        button_height = 35 if self.screen_width <= 1366 else 45
        clear_btn.setFixedHeight(button_height)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        clear_btn.clicked.connect(self.clear_cart)
        buttons_layout.addWidget(clear_btn)
        
        # Botón pagar más compacto
        pay_btn = QPushButton("� Crear Orden")  # Cambiar texto
        pay_btn.setFixedHeight(button_height)
        pay_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        pay_btn.clicked.connect(self.create_order)
        buttons_layout.addWidget(pay_btn)
        
        layout.addLayout(buttons_layout)
        
        return panel
    
    def load_categories(self):
        """Cargar categorías como botones"""
        categories = self.product_controller.get_all_categories()
        
        category_icons = {
            "Hamburguesas": "🍔",
            "Bebidas": "🥤", 
            "Acompañamientos": "🍟",
            "Postres": "🍰"
        }
        
        # Buscar el frame de categorías dentro del scroll area
        categories_frame = None
        for i in range(self.pos_view.layout().itemAt(0).widget().layout().count()):
            item = self.pos_view.layout().itemAt(0).widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QScrollArea):
                # Es el scroll area de categorías
                scroll_widget = item.widget().widget()
                if scroll_widget and isinstance(scroll_widget, QFrame):
                    categories_frame = scroll_widget
                    break
        
        if not categories_frame:
            return
            
        categories_layout = categories_frame.layout()
        
        # Estilo para botones de categorías con tamaño responsivo y fijo
        padding = "8px 12px" if self.is_small_screen else "10px 16px"
        font_size = 12 if self.is_small_screen else 13
        min_width = 100 if self.is_small_screen else 120
        
        category_button_style = f"""
            QPushButton {{
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                padding: {padding};
                border-radius: 10px;
                font-weight: bold;
                font-size: {font_size}px;
                min-width: {min_width}px;
                max-width: {min_width + 50}px;
                height: 40px;
            }}
            QPushButton:checked {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: 2px solid {ColorPalette.OXFORD_BLUE};
            }}
            QPushButton:hover {{
                border: 2px solid {ColorPalette.YINMN_BLUE};
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
            }}
            QPushButton:checked:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """
        
        # Aplicar estilo al botón "Todas" existente
        self.category_buttons[0].setStyleSheet(category_button_style)
        self.category_buttons[0].setMinimumWidth(min_width)
        self.category_buttons[0].setFixedHeight(40)
        
        # Agregar botones de categorías específicas
        for category in categories:
            icon = category_icons.get(category.name, "🍴")
            btn_text = f"{icon} {category.name}"
            
            btn = QPushButton(btn_text)
            btn.setCheckable(True)
            btn.setStyleSheet(category_button_style)
            btn.setMinimumWidth(min_width)
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda checked, cat_id=category.id, button=btn: self.select_category(cat_id, button))
            
            self.category_buttons.append(btn)
            categories_layout.addWidget(btn)
        
        # NO agregar stretch al final para permitir scroll horizontal
        # categories_layout.addStretch()  # Comentado para permitir scroll
        
        # Cargar todos los productos por defecto
        self.load_products()
    
    def select_category(self, category_id, button):
        """Seleccionar una categoría y actualizar productos"""
        # Desmarcar todos los botones
        for btn in self.category_buttons:
            btn.setChecked(False)
        
        # Marcar el botón seleccionado
        button.setChecked(True)
        self.selected_category_id = category_id
        
        # Cargar productos de la categoría
        self.load_products()
    
    def load_products(self):
        """Cargar productos según la categoría seleccionada con grid responsivo"""
        # Limpiar productos actuales
        for i in reversed(range(self.products_layout.count())):
            child = self.products_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Obtener productos
        if self.selected_category_id is None:
            products = self.product_controller.get_all_products()
        else:
            products = self.product_controller.get_products_by_category(self.selected_category_id)
        
        # Usar la función optimizada para calcular columnas
        columns = self.get_optimal_columns()
        
        # Mostrar productos en grid responsivo
        row, col = 0, 0
        
        for product in products:
            btn = self.create_product_button(product)
            self.products_layout.addWidget(btn, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1
    
    def create_product_button(self, product):
        """Crear botón de producto con diseño responsivo optimizado"""
        container = QFrame()
        
        # Calcular tamaño de botón basado en el ancho disponible actual
        current_width = self.width()
        available_width = int(current_width * 0.75) - 40  # 75% menos márgenes
        columns = self.get_optimal_columns()
        
        # Calcular ancho óptimo por botón
        spacing = 10 if self.is_small_screen else 12
        button_width = max(200, (available_width - (spacing * (columns - 1))) // columns)
        
        # Ajustar altura proporcionalmente
        if self.is_small_screen:
            button_height = min(150, int(button_width * 0.5))  # Relación 2:1
            font_size_name = 12
            font_size_price = 15
            padding_container = 8
            padding_name = 5
        else:
            button_height = min(160, int(button_width * 0.55))  # Relación 1.8:1
            font_size_name = 14
            font_size_price = 16
            padding_container = 10
            padding_name = 6
        
        container.setFixedSize(button_width, button_height)
        container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.PLATINUM},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)});
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 12px;
                padding: {padding_container}px;
            }}
            QFrame:hover {{
                border: 2px solid {ColorPalette.YINMN_BLUE};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)});
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(4)
        layout.setContentsMargins(padding_container, padding_container, padding_container, padding_container)
        
        
        # Nombre del producto
        name_label = QLabel(product.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet(f"""
            font-size: {font_size_name}px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            padding: {padding_name}px;
            background: transparent;
        """)
        layout.addWidget(name_label)
        
        # Precio
        price_label = QLabel(f"$ {product.price:,.0f}")
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setStyleSheet(f"""
            font-size: {font_size_price}px;
            font-weight: bold;
            color: {ColorPalette.SUCCESS};
            background: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.1)};
            border-radius: 8px;
            padding: 6px;
        """)
        layout.addWidget(price_label)
        
        # Hacer clickeable todo el contenedor
        container.mousePressEvent = lambda event: self.add_to_cart(product)
        container.setCursor(Qt.PointingHandCursor)
        
        return container
    
    def add_to_cart(self, product):
        """Agregar producto al carrito"""
        if product.id in self.cart_items:
            self.cart_items[product.id]['quantity'] += 1
        else:
            self.cart_items[product.id] = {
                'product': product,
                'quantity': 1
            }
        
        self.update_cart_display()
        
        # Animación visual del botón
        self.animate_add_to_cart()
    
    def animate_add_to_cart(self):
        """Pequeña animación al agregar producto"""
        # Aquí podrías agregar una animación más elaborada
        pass
    
    def update_cart_display(self):
        """Actualizar la visualización del carrito"""
        # Limpiar items actuales
        for i in reversed(range(self.cart_layout.count())):
            child = self.cart_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        total = 0
        total_items = 0
        
        # Agregar items del carrito
        for item_data in self.cart_items.values():
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Crear widget del item
            item_widget = CartItemWidget(product, quantity)
            item_widget.quantity_changed.connect(self.update_item_quantity)
            item_widget.item_removed.connect(self.remove_item)
            
            self.cart_layout.addWidget(item_widget)
            
            # Calcular totales
            subtotal = product.price * quantity
            total += subtotal
            total_items += quantity
        
        # Actualizar labels de totales
        self.items_count_label.setText(f"{total_items} producto{'s' if total_items != 1 else ''}")
        self.total_label.setText(f"Total: ${total:,.0f}")
        
        # Mostrar mensaje si carrito vacío
        if not self.cart_items:
            empty_label = QLabel("🛒 Carrito vacío\nAgrega productos del menú")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet(f"""
                color: {ColorPalette.SILVER_LAKE_BLUE};
                font-size: 16px;
                font-weight: bold;
                padding: 40px;
            """)
            self.cart_layout.addWidget(empty_label)
    
    def update_item_quantity(self, product_id, new_quantity):
        """Actualizar cantidad de un item"""
        if product_id in self.cart_items:
            self.cart_items[product_id]['quantity'] = new_quantity
            self.update_cart_display()
    
    def remove_item(self, product_id):
        """Remover item del carrito"""
        if product_id in self.cart_items:
            del self.cart_items[product_id]
            self.update_cart_display()
    
    def clear_cart(self):
        """Limpiar carrito completo"""
        if self.cart_items:
            reply = QMessageBox.question(
                self, 'Confirmar', 
                '¿Estás seguro de que quieres limpiar el carrito?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.cart_items.clear()
                self.update_cart_display()
    
    def create_order(self):
        """Crear orden pendiente (sin pago)"""
        if not self.cart_items:
            QMessageBox.warning(self, "Carrito Vacío", "Agrega productos antes de crear la orden")
            return
        
        # Calcular total
        total = sum(item_data['product'].price * item_data['quantity'] for item_data in self.cart_items.values())
        
        # Dialog para información del cliente (sin método de pago)
        dialog = CustomerInfoDialog(total, self, payment_required=False)
        if dialog.exec_() == QDialog.Accepted:
            customer_info = dialog.get_customer_info()
            
            try:
                # Convertir carrito a formato para el controlador
                order_items = []
                for item_data in self.cart_items.values():
                    order_items.append({
                        'product_id': item_data['product'].id,
                        'quantity': item_data['quantity']
                    })
                
                # Crear orden (estado PENDING por defecto)
                order = self.order_controller.create_order(
                    order_items, 
                    customer_info['name'],
                    customer_info['table']
                )
                
                # Imprimir ticket de orden (no recibo de pago)
                cart_list = list(self.cart_items.values())
                self.printer.print_order_ticket(order, cart_list)
                
                # Mostrar confirmación
                table_info = f" - Mesa {customer_info['table']}" if customer_info['table'] else " - Para llevar"
                
                message = f"""
                ✅ ¡Orden creada exitosamente!
                
                Orden: #{order.id}
                Cliente: {customer_info['name']}{table_info}
                Total: ${order.total:,.0f}
                Estado: Pendiente para cocina
                
                El ticket se ha enviado a impresión.
                El pago se realizará al final del servicio.
                """
                
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Orden Creada")
                msg_box.setText(message)
                msg_box.setStyleSheet(f"""
                    QMessageBox {{
                        background-color: {ColorPalette.PLATINUM};
                    }}
                    QMessageBox QLabel {{
                        color: {ColorPalette.RICH_BLACK};
                        font-size: 14px;
                    }}
                """)
                msg_box.exec_()
                
                # Limpiar carrito
                self.cart_items.clear()
                self.update_cart_display()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear la orden:\n{str(e)}")
    
    def open_kitchen_window(self):
        """Cambiar a la vista de cocina"""
        if not self.kitchen_view:
            # Importar aquí para evitar importación circular
            from views.kitchen_orders_window import KitchenOrdersView
            self.kitchen_view = KitchenOrdersView(self)
            self.kitchen_view.back_to_pos.connect(self.show_pos_view)
            self.kitchen_view.open_history.connect(self.open_payment_history)
            self.stack_widget.addWidget(self.kitchen_view)
        else:
            # Actualizar órdenes al abrir la vista de cocina
            self.kitchen_view.load_orders()
        
        self.stack_widget.setCurrentWidget(self.kitchen_view)
    
    def open_payment_history(self):
        """Cambiar a la vista de historial de pagos"""
        if not self.payment_history_view:
            # Importar aquí para evitar importación circular
            from views.payment_history_window import PaymentHistoryView
            self.payment_history_view = PaymentHistoryView(self)
            self.payment_history_view.back_to_pos.connect(self.show_pos_view)
            self.payment_history_view.open_kitchen.connect(self.open_kitchen_window)
            self.stack_widget.addWidget(self.payment_history_view)
        
        # Refrescar datos cada vez que se abre el historial
        self.payment_history_view.refresh_data()
        self.stack_widget.setCurrentWidget(self.payment_history_view)
    
    def show_pos_view(self):
        """Volver a la vista de POS"""
        self.stack_widget.setCurrentWidget(self.pos_view)
    
    def resizeEvent(self, event):
        """Manejar el redimensionamiento de la ventana"""
        super().resizeEvent(event)
        
        # Actualizar información de pantalla
        new_width = event.size().width()
        new_height = event.size().height()
        
        print(f"🔄 Redimensionando ventana: {new_width}x{new_height}")
        
        # Si el cambio de tamaño es significativo, recalcular el grid
        if hasattr(self, 'screen_width'):
            width_diff = abs(new_width - self.width() if hasattr(self, '_last_width') else 0)
            
            # Actualizar dimensiones
            self._last_width = new_width
            self.screen_width = new_width
            self.screen_height = new_height
            
            # Recalcular si es pantalla pequeña
            old_is_small = self.is_small_screen
            self.is_small_screen = new_width <= 1366
            
            # Recargar productos si hay cambio significativo o cambió la categoría de tamaño
            if width_diff > 50 or old_is_small != self.is_small_screen:
                print(f"🔄 Recalculando grid por cambio significativo: diff={width_diff}, pequeña={self.is_small_screen}")
                # Usar QTimer para evitar múltiples recálculos rápidos
                if hasattr(self, '_resize_timer'):
                    self._resize_timer.stop()
                
                from PyQt5.QtCore import QTimer
                self._resize_timer = QTimer()
                self._resize_timer.setSingleShot(True)
                self._resize_timer.timeout.connect(self.load_products)
                self._resize_timer.start(100)  # Esperar 100ms antes de recalcular
    
    def handle_logout(self):
        """Manejar solicitud de logout"""
        reply = QMessageBox.question(self, "Cerrar Sesión", 
                                   "¿Estás seguro de que deseas cerrar sesión?",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.logout_requested.emit()
    
    def get_optimal_columns(self):
        """Calcular número óptimo de columnas según el ancho actual real de la ventana"""
        # Obtener el ancho real actual de la ventana
        current_width = self.width()
        
        # Calcular ancho disponible para productos (75% del total menos márgenes)
        available_width = int(current_width * 0.75) - 40  # Restar márgenes y espaciado
        
        # Ancho mínimo por botón según el tipo de pantalla
        if self.is_small_screen:
            button_width = 300  # Botones más grandes para pantallas pequeñas
            min_spacing = 10
        else:
            button_width = 220  # Botones estándar para pantallas grandes
            min_spacing = 12
        
        # Calcular número de columnas que caben
        columns = max(1, available_width // (button_width + min_spacing))
        
        # Limitar máximo de columnas según resolución
        if self.is_small_screen:
            columns = min(columns, 4)  # Máximo 4 columnas en pantallas pequeñas
        else:
            columns = min(columns, 6)  # Máximo 6 columnas en pantallas grandes
        
        print(f"📐 Cálculo de columnas: ancho_ventana={current_width}, ancho_productos={available_width}, columnas={columns}")
        return int(columns)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = POSWindow()
    window.show()
    sys.exit(app.exec_())