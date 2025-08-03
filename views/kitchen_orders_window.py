# views/kitchen_orders_window.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.order_controller import OrderController
from models.order import OrderStatus
from datetime import datetime
from utils.colors import ColorPalette, CommonStyles

class OrderCard(QFrame):
    """Widget individual para mostrar cada pedido como sticky note"""
    
    status_changed = pyqtSignal(int, OrderStatus)  # Señal para cambio de estado
    
    def __init__(self, order):
        super().__init__()
        self.order = order
        self.init_ui()
    
    def init_ui(self):
        self.setFixedSize(280, 320)
        self.setFrameStyle(QFrame.Box)
        self.setAttribute(Qt.WA_StyledBackground)
        
        # Estilo del card según el estado
        self.update_card_style()
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header con número de orden y tiempo
        header_layout = QHBoxLayout()
        
        order_label = QLabel(f"ORDEN #{self.order.id}")
        order_label.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {ColorPalette.RICH_BLACK};")
        header_layout.addWidget(order_label)
        
        header_layout.addStretch()
        
        # Tiempo transcurrido
        elapsed = datetime.now() - self.order.created_at
        minutes = int(elapsed.total_seconds() / 60)
        time_label = QLabel(f"{minutes}min")
        time_label.setStyleSheet(f"font-size: 12px; color: {ColorPalette.SILVER_LAKE_BLUE}; font-weight: bold;")
        header_layout.addWidget(time_label)
        
        layout.addLayout(header_layout)
        
        # Información del cliente
        if self.order.table_number:
            customer_info = f"{self.order.customer_name} - Mesa {self.order.table_number}"
        else:
            customer_info = self.order.customer_name
        
        customer_label = QLabel(customer_info)
        customer_label.setStyleSheet(f"font-size: 14px; color: {ColorPalette.RICH_BLACK}; font-weight: 500;")
        layout.addWidget(customer_label)
        
        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE};")
        layout.addWidget(line)
        
        # Items del pedido
        items_scroll = QScrollArea()
        items_scroll.setWidgetResizable(True)
        items_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        items_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        items_scroll.setMaximumHeight(120)
        
        items_widget = QWidget()
        items_layout = QVBoxLayout(items_widget)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(4)
        
        for item in self.order.items:
            item_label = QLabel(f"{item.quantity}x {item.product.name}")
            item_label.setStyleSheet(f"font-size: 13px; color: {ColorPalette.RICH_BLACK}; padding: 2px;")
            items_layout.addWidget(item_label)
        
        items_scroll.setWidget(items_widget)
        layout.addWidget(items_scroll)
        
        # Estado actual
        status_label = QLabel(f"Estado: {self.order.status_display}")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(f"""
            background-color: {self.order.status_color};
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding: 8px;
            border-radius: 15px;
        """)
        layout.addWidget(status_label)
        
        # Botones de acción
        if self.order.status != OrderStatus.DELIVERED and self.order.status != OrderStatus.CANCELLED:
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(5)
            
            if self.order.status == OrderStatus.PENDING:
                start_btn = QPushButton("Iniciar")
                start_btn.setStyleSheet(CommonStyles.button_primary())
                start_btn.clicked.connect(lambda: self.change_status(OrderStatus.PREPARING))
                buttons_layout.addWidget(start_btn)
            
            elif self.order.status == OrderStatus.PREPARING:
                ready_btn = QPushButton("Listo")
                ready_btn.setStyleSheet(CommonStyles.button_success())
                ready_btn.clicked.connect(lambda: self.change_status(OrderStatus.READY))
                buttons_layout.addWidget(ready_btn)
            
            elif self.order.status == OrderStatus.READY:
                deliver_btn = QPushButton("Entregar")
                deliver_btn.setStyleSheet(CommonStyles.button_secondary())
                deliver_btn.clicked.connect(lambda: self.change_status(OrderStatus.DELIVERED))
                buttons_layout.addWidget(deliver_btn)
            
            # Botón cancelar (siempre disponible para órdenes activas)
            if self.order.status != OrderStatus.DELIVERED:
                cancel_btn = QPushButton("✕")
                cancel_btn.setFixedSize(30, 30)
                cancel_btn.setStyleSheet(CommonStyles.button_danger())
                cancel_btn.clicked.connect(lambda: self.change_status(OrderStatus.CANCELLED))
                buttons_layout.addWidget(cancel_btn)
            
            layout.addLayout(buttons_layout)
        
        # Total
        total_label = QLabel(f"Total: ${self.order.total:.2f}")
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet(f"font-weight: bold; font-size: 15px; color: {ColorPalette.RICH_BLACK}; margin-top: 5px;")
        layout.addWidget(total_label)
    
    def update_card_style(self):
        """Actualizar estilo del card según el estado"""
        border_color = self.order.status_color
        self.setStyleSheet(f"""
            OrderCard {{
                background-color: {ColorPalette.PLATINUM};
                border: 3px solid {border_color};
                border-radius: 15px;
                margin: 5px;
            }}
            OrderCard:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
            }}
        """)
    
    def get_button_style(self, color):
        """Generar estilo para botones"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}bb;
            }}
        """
    
    def change_status(self, new_status):
        """Emitir señal de cambio de estado"""
        self.status_changed.emit(self.order.id, new_status)

class KitchenOrdersView(QWidget):
    """Vista para mostrar estado de pedidos"""
    
    back_to_pos = pyqtSignal()  # Señal para volver a POS
    open_history = pyqtSignal()  # Señal para abrir historial
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order_controller = OrderController()
        self.init_ui()
        self.load_orders()
        
        # Timer para actualizar automáticamente
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_orders)
        self.timer.start(10000)  # Actualizar cada 10 segundos
    
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🍳 ESTADO DE PEDIDOS")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 10px;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Botón actualizar
        # Botón volver a POS
        pos_btn = QPushButton("🍽️ Volver a POS")
        pos_btn.setStyleSheet(CommonStyles.button_success())
        pos_btn.clicked.connect(lambda: self.back_to_pos.emit())
        header_layout.addWidget(pos_btn)
        
        # Botón historial de pagos
        history_btn = QPushButton("💰 Historial")
        history_btn.setStyleSheet(CommonStyles.button_primary())
        history_btn.clicked.connect(lambda: self.open_history.emit())
        header_layout.addWidget(history_btn)
        
        # Botón actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setStyleSheet(CommonStyles.button_secondary())
        refresh_btn.clicked.connect(self.load_orders)
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        
        # Área de scroll para las cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Widget contenedor de las cards
        self.orders_container = QWidget()
        self.orders_layout = QGridLayout(self.orders_container)
        self.orders_layout.setSpacing(15)
        self.orders_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        scroll_area.setWidget(self.orders_container)
        main_layout.addWidget(scroll_area)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
    
    def load_orders(self):
        """Cargar y mostrar pedidos activos"""
        # Limpiar cards existentes
        for i in reversed(range(self.orders_layout.count())):
            child = self.orders_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Obtener pedidos activos
        orders = self.order_controller.get_active_orders()
        
        if not orders:
            # Mostrar mensaje si no hay pedidos
            no_orders_label = QLabel("🎉 ¡No hay pedidos pendientes!")
            no_orders_label.setAlignment(Qt.AlignCenter)
            no_orders_label.setStyleSheet(f"""
                font-size: 24px;
                color: {ColorPalette.SILVER_LAKE_BLUE};
                font-weight: bold;
                margin: 50px;
            """)
            self.orders_layout.addWidget(no_orders_label, 0, 0)
            return
        
        # Mostrar pedidos en grid
        row, col = 0, 0
        max_cols = 4  # 4 columnas
        
        for order in orders:
            card = OrderCard(order)
            card.status_changed.connect(self.update_order_status)
            
            self.orders_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def update_order_status(self, order_id, new_status):
        """Actualizar estado de un pedido"""
        try:
            self.order_controller.update_order_status(order_id, new_status)
            self.load_orders()  # Recargar vista
            
            # Mostrar notificación
            status_text = {
                OrderStatus.PREPARING: "iniciado",
                OrderStatus.READY: "completado",
                OrderStatus.DELIVERED: "entregado",
                OrderStatus.CANCELLED: "cancelado"
            }.get(new_status, "actualizado")
            
            QMessageBox.information(
                self, 
                "Estado Actualizado", 
                f"Pedido #{order_id} {status_text} correctamente"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar estado: {str(e)}")

