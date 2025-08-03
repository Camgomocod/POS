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
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Nombre del producto
        name_label = QLabel(self.product.name)
        name_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.RICH_BLACK};")
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        # Controles de cantidad
        qty_layout = QHBoxLayout()
        
        minus_btn = QPushButton("-")
        minus_btn.setFixedSize(25, 25)
        minus_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)}; }}
        """)
        minus_btn.clicked.connect(self.decrease_quantity)
        qty_layout.addWidget(minus_btn)
        
        self.qty_label = QLabel(str(self.quantity))
        self.qty_label.setAlignment(Qt.AlignCenter)
        self.qty_label.setFixedWidth(30)
        self.qty_label.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {ColorPalette.RICH_BLACK};")
        qty_layout.addWidget(self.qty_label)
        
        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(25, 25)
        plus_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)}; }}
        """)
        plus_btn.clicked.connect(self.increase_quantity)
        qty_layout.addWidget(plus_btn)
        
        layout.addLayout(qty_layout)
        
        # Precio
        price_label = QLabel(f"${self.product.price * self.quantity:.2f}")
        price_label.setStyleSheet(f"font-weight: bold; color: {ColorPalette.SUCCESS}; margin-left: 10px;")
        price_label.setFixedWidth(60)
        price_label.setAlignment(Qt.AlignRight)
        layout.addWidget(price_label)
        
        # Botón eliminar
        remove_btn = QPushButton("✕")
        remove_btn.setFixedSize(25, 25)
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {ColorPalette.OXFORD_BLUE}; }}
        """)
        remove_btn.clicked.connect(lambda: self.item_removed.emit(self.product.id))
        layout.addWidget(remove_btn)
        
        # Estilo del widget
        self.setStyleSheet(f"""
            CartItemWidget {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 10px;
                margin: 2px;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
            }}
            CartItemWidget:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
            }}
        """)
    
    def increase_quantity(self):
        self.quantity += 1
        self.qty_label.setText(str(self.quantity))
        self.quantity_changed.emit(self.product.id, self.quantity)
    
    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.qty_label.setText(str(self.quantity))
            self.quantity_changed.emit(self.product.id, self.quantity)

class CustomerInfoDialog(QDialog):
    """Dialog para capturar información del cliente y método de pago"""
    
    def __init__(self, total_amount, parent=None):
        super().__init__(parent)
        self.total_amount = total_amount
        self.setWindowTitle("Información del Pedido")
        self.setFixedSize(380, 420)  # Tamaño compacto
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
        
        total_label = QLabel(f"Total: ${self.total_amount:.2f}")
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
                border-color: {ColorPalette.YINMN_BLUE};
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
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        layout.addWidget(self.table_input)
        
        # Método de pago compacto
        payment_title = QLabel("Método de Pago:")
        payment_title.setStyleSheet(f"""
            font-weight: bold; 
            color: {ColorPalette.RICH_BLACK}; 
            font-size: 13px;
            margin-top: 5px;
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
                    text-align: center;
                }}
                QPushButton:checked {{
                    background-color: {ColorPalette.YINMN_BLUE};
                    color: {ColorPalette.PLATINUM};
                    border-color: {ColorPalette.OXFORD_BLUE};
                }}
                QPushButton:hover {{
                    border-color: {ColorPalette.YINMN_BLUE};
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
        return {
            'name': self.name_input.text().strip() or "Cliente",
            'table': self.table_input.value() if self.table_input.value() > 0 else None,
            'payment_method': self.payment_method
        }

class POSWindow(QMainWindow):
    """Ventana POS mejorada con diseño moderno"""
    
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
        self.setGeometry(100, 100, 1500, 950)  # Tamaño aumentado para mejor distribución
        
        # Layout principal para la vista POS
        main_layout = QHBoxLayout(self.pos_view)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Panel izquierdo - Productos (70% del espacio)
        left_panel = self.create_product_panel()
        main_layout.addWidget(left_panel, 7)  # Proporción aumentada
        
        # Panel derecho - Carrito (30% del espacio)
        right_panel = self.create_cart_panel()
        main_layout.addWidget(right_panel, 3)  # Proporción optimizada
        
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
        layout.setSpacing(15)
        
        # Header del panel
        header_layout = QHBoxLayout()
        
        title = QLabel("🍽️ MENÚ")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet(f"""
            font-size: 26px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 5px;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Botón abrir cocina
        kitchen_btn = QPushButton("👨‍🍳 Cocina")
        kitchen_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.WARNING};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 12px 18px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)}; }}
        """)
        kitchen_btn.clicked.connect(self.open_kitchen_window)
        header_layout.addWidget(kitchen_btn)
        
        # Botón historial de pagos
        history_btn = QPushButton("💰 Historial")
        history_btn.setStyleSheet(CommonStyles.button_primary())
        history_btn.clicked.connect(self.open_payment_history)
        header_layout.addWidget(history_btn)
        
        layout.addLayout(header_layout)
        
        # Botones de categorías (horizontal)
        categories_frame = QFrame()
        categories_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                border-radius: 12px;
                padding: 10px;
            }}
        """)
        categories_layout = QHBoxLayout(categories_frame)
        categories_layout.setSpacing(8)
        
        # Crear botones de categorías
        self.category_buttons = []
        self.selected_category_id = None
        
        # Botón "Todas"
        all_btn = QPushButton("🍽️ Todas")
        all_btn.setCheckable(True)
        all_btn.setChecked(True)  # Por defecto seleccionado
        all_btn.clicked.connect(lambda: self.select_category(None, all_btn))
        self.category_buttons.append(all_btn)
        categories_layout.addWidget(all_btn)
        
        layout.addWidget(categories_frame)
        
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
        self.products_layout.setSpacing(12)  # Espaciado optimizado
        self.products_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Alineación izquierda
        self.products_layout.setContentsMargins(15, 15, 15, 15)
        
        scroll.setWidget(self.products_widget)
        layout.addWidget(scroll)
        
        return panel
    
    def create_cart_panel(self):
        panel = QFrame()
        panel.setStyleSheet(CommonStyles.panel_main())
        panel.setMinimumWidth(380)  # Ancho mínimo para el panel del carrito
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Header del carrito mejorado
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: {ColorPalette.gradient_primary()};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("🛒 ORDEN ACTUAL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {ColorPalette.PLATINUM};
            margin-bottom: 5px;
        """)
        header_layout.addWidget(title)
        
        # Contador de items en el header
        self.items_count_label = QLabel("0 productos")
        self.items_count_label.setAlignment(Qt.AlignCenter)
        self.items_count_label.setStyleSheet(f"color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.9)}; font-size: 14px; font-weight: bold;")
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
                border-radius: 10px;
            }}
            QScrollBar:vertical {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 4px;
                min-height: 20px;
            }}
        """)
        
        self.cart_container = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container)
        self.cart_layout.setAlignment(Qt.AlignTop)
        self.cart_layout.setSpacing(6)
        self.cart_layout.setContentsMargins(5, 5, 5, 5)
        
        cart_scroll.setWidget(self.cart_container)
        layout.addWidget(cart_scroll)
        
        # Resumen del total con mejor diseño
        total_frame = QFrame()
        total_frame.setStyleSheet(f"""
            QFrame {{
                background: {ColorPalette.gradient_secondary()};
                border-radius: 15px;
                padding: 20px;
                border: 1px solid {ColorPalette.OXFORD_BLUE};
            }}
        """)
        total_layout = QVBoxLayout(total_frame)
        
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet(f"color: {ColorPalette.PLATINUM}; font-size: 26px; font-weight: bold;")
        total_layout.addWidget(self.total_label)
        
        layout.addWidget(total_frame)
        
        # Botones de acción con mejor espaciado
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(12)
        
        # Botón limpiar carrito
        clear_btn = QPushButton("🗑️ Limpiar Carrito")
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 12px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        clear_btn.clicked.connect(self.clear_cart)
        buttons_layout.addWidget(clear_btn)
        
        # Botón procesar pago (principal)
        pay_btn = QPushButton("💳 PROCESAR PAGO")
        pay_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ColorPalette.gradient_primary()};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 20px;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {ColorPalette.YINMN_BLUE};
            }}
            QPushButton:pressed {{
                background: {ColorPalette.OXFORD_BLUE};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.7)};
            }}
        """)
        pay_btn.clicked.connect(self.process_payment)
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
        
        # Buscar el frame de categorías
        categories_frame = None
        for i in range(self.pos_view.layout().itemAt(0).widget().layout().count()):
            item = self.pos_view.layout().itemAt(0).widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QFrame):
                # Verificar si tiene layout horizontal
                if isinstance(item.widget().layout(), QHBoxLayout):
                    categories_frame = item.widget()
                    break
        
        if not categories_frame:
            return
            
        categories_layout = categories_frame.layout()
        
        # Estilo para botones de categorías
        category_button_style = f"""
            QPushButton {{
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                padding: 12px 16px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }}
            QPushButton:checked {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border-color: {ColorPalette.OXFORD_BLUE};
            }}
            QPushButton:hover {{
                border-color: {ColorPalette.YINMN_BLUE};
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
            }}
            QPushButton:checked:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """
        
        # Aplicar estilo al botón "Todas"
        self.category_buttons[0].setStyleSheet(category_button_style)
        
        # Agregar botones de categorías específicas
        for category in categories:
            icon = category_icons.get(category.name, "🍴")
            btn_text = f"{icon} {category.name}"
            
            btn = QPushButton(btn_text)
            btn.setCheckable(True)
            btn.setStyleSheet(category_button_style)
            btn.clicked.connect(lambda checked, cat_id=category.id, button=btn: self.select_category(cat_id, button))
            
            self.category_buttons.append(btn)
            categories_layout.addWidget(btn)
        
        categories_layout.addStretch()  # Espaciador al final
        
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
        """Cargar productos según la categoría seleccionada"""
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
        
        # Mostrar productos en grid (4 columnas para mejor aprovechamiento del espacio)
        row, col = 0, 0
        columns = 4  # Aumentado a 4 columnas
        
        for product in products:
            btn = self.create_product_button(product)
            self.products_layout.addWidget(btn, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1
    
    def create_product_button(self, product):
        """Crear botón de producto con diseño moderno y tamaño optimizado"""
        container = QFrame()
        container.setFixedSize(220, 160)  # Tamaño optimizado para 4 columnas
        container.setCursor(Qt.PointingHandCursor)
        
        # Layout interno
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 15, 12, 12)
        layout.setSpacing(8)
        
        # Contenedor para el nombre
        name_container = QWidget()
        name_layout = QVBoxLayout(name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(0)
        
        # Nombre del producto
        name_label = QLabel(product.name)
        name_label.setStyleSheet(f"""
            color: {ColorPalette.RICH_BLACK};
            font-weight: bold;
            font-size: 14px;
            background-color: transparent;
            padding: 6px;
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setMinimumHeight(50)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        name_layout.addWidget(name_label)
        
        layout.addWidget(name_container, 3)
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background-color: {ColorPalette.SILVER_LAKE_BLUE}; max-height: 1px;")
        layout.addWidget(line)
        
        # Precio
        price_label = QLabel(f"${product.price:.2f}")
        price_label.setStyleSheet(f"""
            color: {ColorPalette.SUCCESS};
            font-weight: bold;
            font-size: 16px;
            background-color: transparent;
            padding: 4px;
        """)
        price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(price_label, 1)
        
        # Estilo del contenedor
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 12px;
            }}
            QFrame:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        
        # Evento de clic
        container.mousePressEvent = lambda e: self.add_to_cart(product)
        
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
        self.total_label.setText(f"Total: ${total:.2f}")
        
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
    
    def process_payment(self):
        """Procesar el pago"""
        if not self.cart_items:
            QMessageBox.warning(self, "Carrito Vacío", "Agrega productos antes de procesar el pago")
            return
        
        # Calcular total
        total = sum(item_data['product'].price * item_data['quantity'] for item_data in self.cart_items.values())
        
        # Dialog para información del cliente con método de pago
        dialog = CustomerInfoDialog(total, self)
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
                
                # Crear orden
                order = self.order_controller.create_order(
                    order_items, 
                    customer_info['name'],
                    customer_info['table']
                )
                
                # Marcar orden como pagada con el método de pago
                self.order_controller.complete_payment(order.id, customer_info['payment_method'])
                
                # Imprimir recibo
                cart_list = list(self.cart_items.values())
                self.printer.print_receipt(order, cart_list)
                
                # Mostrar confirmación
                table_info = f" - Mesa {customer_info['table']}" if customer_info['table'] else " - Para llevar"
                payment_methods = {
                    'efectivo': '💵 Efectivo',
                    'transferencia': '🏦 Transferencia',
                    'tarjeta': '💳 Tarjeta'
                }
                payment_display = payment_methods.get(customer_info['payment_method'], customer_info['payment_method'])
                
                message = f"""
                ✅ ¡Pedido procesado exitosamente!
                
                Orden: #{order.id}
                Cliente: {customer_info['name']}{table_info}
                Total: ${order.total:.2f}
                Método de Pago: {payment_display}
                
                El recibo se ha enviado a impresión.
                """
                
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Pedido Procesado")
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
                QMessageBox.critical(self, "Error", f"Error al procesar el pedido:\n{str(e)}")
    
    def open_kitchen_window(self):
        """Cambiar a la vista de cocina"""
        if not self.kitchen_view:
            # Importar aquí para evitar importación circular
            from views.kitchen_orders_window import KitchenOrdersView
            self.kitchen_view = KitchenOrdersView(self)
            self.kitchen_view.back_to_pos.connect(self.show_pos_view)
            self.kitchen_view.open_history.connect(self.open_payment_history)
            self.stack_widget.addWidget(self.kitchen_view)
        
        self.stack_widget.setCurrentWidget(self.kitchen_view)
    
    def open_payment_history(self):
        """Cambiar a la vista de historial de pagos"""
        if not self.payment_history_view:
            # Importar aquí para evitar importación circular
            from views.payment_history_window import PaymentHistoryView
            self.payment_history_view = PaymentHistoryView(self)
            self.payment_history_view.back_to_pos.connect(self.show_pos_view)
            self.stack_widget.addWidget(self.payment_history_view)
        
        # Refrescar datos cada vez que se abre el historial
        self.payment_history_view.refresh_data()
        self.stack_widget.setCurrentWidget(self.payment_history_view)
    
    def show_pos_view(self):
        """Volver a la vista de POS"""
        self.stack_widget.setCurrentWidget(self.pos_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = POSWindow()
    window.show()
    sys.exit(app.exec_())