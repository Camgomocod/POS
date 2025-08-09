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
    """Widget individual para mostrar cada pedido como sticky note mejorado"""
    
    status_changed = pyqtSignal(int, OrderStatus)  # Señal para cambio de estado
    payment_requested = pyqtSignal(int)  # Señal para solicitar pago de una orden
    
    def __init__(self, order):
        super().__init__()
        self.order = order
        self.is_interactive = self.order.status != OrderStatus.PAID.value  # Solo interactivo si no está pagado
        self.init_ui()
    
    def init_ui(self):
        # Tamaño fijo para mantener apariencia consistente
        screen = QApplication.primaryScreen().geometry()
        if screen.width() <= 1366:  # Resoluciones pequeñas (laptops)
            card_width = 300
            card_height = 370
            self.font_sizes = {'header': 14, 'customer': 12, 'items': 10, 'status': 12, 'total': 13}
        else:  # Resoluciones más grandes
            card_width = 300
            card_height = 370
            self.font_sizes = {'header': 16, 'customer': 14, 'items': 12, 'status': 14, 'total': 15}
        
        # Usar tamaño fijo para mantener consistencia visual
        self.setFixedSize(card_width, card_height)
        
        self.setFrameStyle(QFrame.Box)
        self.setAttribute(Qt.WA_StyledBackground)
        
        # Estilo del card según el estado
        self.update_card_style()
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Espaciado más generoso
        layout.setContentsMargins(15, 15, 15, 15)  # Márgenes más amplios
        
        # Header con número de orden y tiempo - simplificado
        header_layout = QHBoxLayout()
        
        order_label = QLabel(f"ORDEN #{self.order.id}")
        order_label.setStyleSheet(f"""
            font-weight: bold; 
            font-size: {self.font_sizes['header']}px; 
            color: {ColorPalette.RICH_BLACK};
        """)
        header_layout.addWidget(order_label)
        
        header_layout.addStretch()
        
        # Tiempo transcurrido - solo mostrar urgencia para estados activos de cocina
        elapsed = datetime.now() - self.order.created_at
        minutes = int(elapsed.total_seconds() / 60)
        
        # Solo aplicar colores de urgencia para estados donde es relevante
        if self.order.status in [OrderStatus.PENDING.value, OrderStatus.PREPARING.value, OrderStatus.READY.value]:
            # Determinar color según urgencia para estados activos
            if minutes > 30:  # Muy urgente
                time_color = ColorPalette.ERROR
                urgency_icon = "🚨"
            elif minutes > 20:  # Urgente
                time_color = ColorPalette.WARNING
                urgency_icon = "⚠️"
            else:
                time_color = ColorPalette.SILVER_LAKE_BLUE
                urgency_icon = "⏱️"
        else:
            # Para pedidos entregados o pagados, usar color neutro sin urgencia
            time_color = ColorPalette.SILVER_LAKE_BLUE
            urgency_icon = "⏱️"
        
        time_label = QLabel(f"{urgency_icon} {minutes}min")
        time_label.setStyleSheet(f"""
            font-size: {self.font_sizes['items']}px; 
            color: {time_color}; 
            font-weight: bold;
        """)
        header_layout.addWidget(time_label)
        
        layout.addLayout(header_layout)
        
        # Información del cliente - más simple y visible
        if self.order.table_number:
            customer_info = f"{self.order.customer_name} - Mesa {self.order.table_number}"
        else:
            customer_info = f"{self.order.customer_name} - Para llevar"
        
        customer_label = QLabel(customer_info)
        customer_label.setStyleSheet(f"""
            font-size: {self.font_sizes['customer']}px; 
            color: {ColorPalette.RICH_BLACK}; 
            font-weight: bold;
            padding: 5px;
            background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
            border-radius: 5px;
            border: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
        """)
        customer_label.setWordWrap(True)
        layout.addWidget(customer_label)
        
        # Línea separadora simple
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {ColorPalette.SILVER_LAKE_BLUE};")
        layout.addWidget(line)
        
        # Items del pedido - diseño compacto para layout vertical
        items_scroll = QScrollArea()
        items_scroll.setWidgetResizable(True)
        items_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        items_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Área de scroll para las cards con altura ajustada para tarjetas fijas
        items_scroll.setMaximumHeight(120 if screen.width() <= 1366 else 140)  
        items_scroll.setMinimumHeight(100 if screen.width() <= 1366 else 120)  
        items_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                background-color: {ColorPalette.PLATINUM};
                padding: 3px;
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
        
        items_widget = QWidget()
        items_layout = QVBoxLayout(items_widget)
        items_layout.setContentsMargins(8, 6, 8, 6)
        items_layout.setSpacing(5)  # Mayor espaciado entre items
        
        for item in self.order.items:
            item_label = QLabel(f"{item.quantity}x {item.product.name}")
            item_label.setStyleSheet(f"""
                color: {ColorPalette.RICH_BLACK};
                font-size: {self.font_sizes['items']}px;
                padding: 8px 10px;
                background-color: #ffffff;
                border-radius: 6px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                font-weight: 500;
                min-height: 24px;
            """)
            item_label.setWordWrap(True)
            item_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            items_layout.addWidget(item_label)
        
        items_scroll.setWidget(items_widget)
        layout.addWidget(items_scroll)
        
        # Estado actual - simple y claro
        status_label = QLabel(f"Estado: {self.order.status_display}")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(f"""
            background-color: {self.order.status_color};
            color: #ffffff;
            font-weight: bold;
            font-size: {self.font_sizes['status']}px;
            padding: 8px;
            border-radius: 8px;
        """)
        layout.addWidget(status_label)
        
        # Botones de acción - simplificados y mejorados
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        # Tamaño de botones
        btn_height = 32 if screen.width() <= 1366 else 36
        
        if self.order.status == OrderStatus.PENDING.value:
            start_btn = QPushButton("🚀 Iniciar")
            start_btn.setFixedHeight(btn_height)
            start_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.YINMN_BLUE};
                    color: #ffffff;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.OXFORD_BLUE};
                }}
            """)
            start_btn.clicked.connect(lambda: self.change_status(OrderStatus.PREPARING))
            buttons_layout.addWidget(start_btn)
        
        elif self.order.status == OrderStatus.PREPARING.value:
            ready_btn = QPushButton("✅ Listo")
            ready_btn.setFixedHeight(btn_height)
            ready_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.SUCCESS};
                    color: #ffffff;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
                }}
            """)
            ready_btn.clicked.connect(lambda: self.change_status(OrderStatus.READY))
            buttons_layout.addWidget(ready_btn)
        
        elif self.order.status == OrderStatus.READY.value:
            deliver_btn = QPushButton("🚚 Entregar")
            deliver_btn.setFixedHeight(btn_height)
            deliver_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.SILVER_LAKE_BLUE};
                    color: #ffffff;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.YINMN_BLUE};
                }}
            """)
            deliver_btn.clicked.connect(lambda: self.change_status(OrderStatus.DELIVERED))
            buttons_layout.addWidget(deliver_btn)
        
        elif self.order.status == OrderStatus.DELIVERED.value:
            # Botón de pago para órdenes entregadas
            pay_btn = QPushButton("💳 Procesar Pago")
            pay_btn.setFixedHeight(btn_height)
            pay_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.WARNING};
                    color: #ffffff;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)};
                }}
            """)
            pay_btn.clicked.connect(self.process_payment)
            buttons_layout.addWidget(pay_btn)
        
        elif self.order.status == OrderStatus.PAID.value:
            # Para pedidos pagados, mostrar solo una etiqueta informativa sin interacción
            paid_label = QLabel("✅ COMPLETADO")
            paid_label.setAlignment(Qt.AlignCenter)
            paid_label.setFixedHeight(btn_height)
            paid_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {ColorPalette.SUCCESS};
                    color: #ffffff;
                    border: 2px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                }}
            """)
            buttons_layout.addWidget(paid_label)
        
        # Botón cancelar (solo para pedidos que no están entregados, pagados o cancelados)
        if self.order.status not in [OrderStatus.DELIVERED.value, OrderStatus.PAID.value, OrderStatus.CANCELLED.value]:
            cancel_btn = QPushButton("❌")
            cancel_btn.setFixedSize(btn_height, btn_height)
            cancel_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.ERROR};
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
                }}
            """)
            cancel_btn.setToolTip("Cancelar pedido")
            cancel_btn.clicked.connect(lambda: self.change_status(OrderStatus.CANCELLED))
            buttons_layout.addWidget(cancel_btn)
        
        # Solo agregar layout si hay botones
        if buttons_layout.count() > 0:
            layout.addLayout(buttons_layout)
        
        # Total - simple y visible
        total_label = QLabel(f"Total: ${self.order.total:.2f}")
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet(f"""
            font-weight: bold; 
            font-size: {self.font_sizes['total']}px; 
            color: {ColorPalette.RICH_BLACK};
            background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.1)};
            padding: 10px 5px 5px 5px;
            border-radius: 5px;
            border: 2px solid {ColorPalette.SUCCESS};
        """)
        layout.addWidget(total_label)
    
    def update_card_style(self):
        """Actualizar estilo del card según el estado - más simple"""
        border_color = self.order.status_color
        
        # Para tarjetas pagadas, usar estilo diferente para indicar que no son interactivas
        if self.order.status == OrderStatus.PAID.value:
            # Estilo para tarjetas completadas/pagadas - sin hover ni efectos de urgencia
            self.setStyleSheet(f"""
                OrderCard {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.8)};
                    border: 2px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.6)};
                    border-radius: 12px;
                    opacity: 0.8;
                }}
            """)
            return
        
        # Solo aplicar efecto visual de urgencia para estados activos de cocina
        if self.order.status in [OrderStatus.PENDING.value, OrderStatus.PREPARING.value, OrderStatus.READY.value]:
            # Efecto visual según urgencia usando border más grueso
            elapsed = datetime.now() - self.order.created_at
            minutes = int(elapsed.total_seconds() / 60)
            
            if minutes > 30:
                border_width = "5px"
                urgency_color = ColorPalette.ERROR
            elif minutes > 20:
                border_width = "4px"
                urgency_color = ColorPalette.WARNING
            else:
                border_width = "3px"
                urgency_color = border_color
        else:
            # Para pedidos entregados, usar borde normal sin urgencia
            border_width = "3px"
            urgency_color = border_color
        
        self.setStyleSheet(f"""
            OrderCard {{
                background-color: {ColorPalette.PLATINUM};
                border: {border_width} solid {urgency_color};
                border-radius: 12px;
            }}
            OrderCard:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.05)};
                border: {border_width} solid {ColorPalette.YINMN_BLUE};
            }}
        """)
    
    def get_button_style(self, color):
        """Generar estilo para botones"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
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
        """Emitir señal de cambio de estado solo si la tarjeta es interactiva"""
        if self.is_interactive:
            self.status_changed.emit(self.order.id, new_status)
    
    def process_payment(self):
        """Emitir señal para procesar pago solo si la tarjeta es interactiva"""
        if self.is_interactive:
            self.payment_requested.emit(self.order.id)

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
        # Detectar resolución para diseño responsivo
        screen = QApplication.primaryScreen().geometry()
        self.is_small_screen = screen.width() <= 1366
        
        # Layout principal optimizado
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)  # Márgenes más compactos
        main_layout.setSpacing(8)
        
        # Header simplificado
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Título simple y claro
        title = QLabel("🍳 ESTADO DE PEDIDOS")
        title_font_size = 22 if self.is_small_screen else 26
        title.setStyleSheet(f"""
            font-size: {title_font_size}px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            padding: 8px 0;
        """)
        header_layout.addWidget(title)
        
        # Estadísticas simplificadas
        self.stats_label = QLabel("📊 Cargando...")
        stats_font_size = 11 if self.is_small_screen else 13
        self.stats_label.setStyleSheet(f"""
            font-size: {stats_font_size}px;
            color: {ColorPalette.RICH_BLACK};
            background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.8)};
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            font-weight: bold;
        """)
        header_layout.addWidget(self.stats_label)
        
        header_layout.addStretch()
        
        # Panel de controles simplificado
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
        
        # Tamaños responsivos para botones
        btn_height = 34 if self.is_small_screen else 40
        btn_font_size = 10 if self.is_small_screen else 12
        
        # Botón volver a POS
        pos_btn = QPushButton("🍽️ POS")
        pos_btn.setFixedHeight(btn_height)
        pos_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: #ffffff;
                border: none;
                padding: 6px 12px;
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
        
        # Botón historial de pagos
        history_btn = QPushButton("💰 Historial")
        history_btn.setFixedHeight(btn_height)
        history_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: {btn_font_size}px;
                min-width: 90px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        history_btn.clicked.connect(lambda: self.open_history.emit())
        controls_layout.addWidget(history_btn)
        
        # Botón actualizar
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setFixedHeight(btn_height)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: {btn_font_size}px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        self.refresh_btn.clicked.connect(self.load_orders)
        controls_layout.addWidget(self.refresh_btn)
        
        header_layout.addWidget(controls_container)
        main_layout.addLayout(header_layout)
        
        # Filtros de estado (nueva funcionalidad)
        filters_container = QFrame()
        filters_container.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.9)};
                border-radius: 6px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                padding: 4px;
            }}
        """)
        filters_layout = QHBoxLayout(filters_container)
        filters_layout.setContentsMargins(8, 6, 8, 6)
        filters_layout.setSpacing(6)
        
        filters_label = QLabel("🎯 Filtrar por estado:")
        filters_label.setStyleSheet(f"""
            font-size: {btn_font_size - 1}px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        filters_layout.addWidget(filters_label)
        
        # Botones de filtro
        self.filter_buttons = {}
        filter_states = [
            ("Todos", None, ColorPalette.RICH_BLACK),
            ("Pendientes", OrderStatus.PENDING, ColorPalette.WARNING),
            ("Preparando", OrderStatus.PREPARING, ColorPalette.YINMN_BLUE),
            ("Listos", OrderStatus.READY, ColorPalette.SUCCESS),
            ("Entregados", OrderStatus.DELIVERED, ColorPalette.SILVER_LAKE_BLUE),
            ("Pagados", OrderStatus.PAID, ColorPalette.SUCCESS)
        ]
        
        self.current_filter = None
        
        for label, status, color in filter_states:
            btn = QPushButton(label)
            btn.setFixedHeight(28 if self.is_small_screen else 32)
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.with_alpha(color, 0.1)};
                    color: {color};
                    border: 2px solid {ColorPalette.with_alpha(color, 0.3)};
                    padding: 4px 8px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: {btn_font_size - 2}px;
                    min-width: 70px;
                }}
                QPushButton:checked {{
                    background-color: {color};
                    color: #ffffff;
                    border: 2px solid {color};
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(color, 0.2)};
                }}
            """)
            btn.clicked.connect(lambda checked, s=status: self.filter_orders(s))
            self.filter_buttons[status] = btn
            filters_layout.addWidget(btn)
        
        # Activar "Todos" por defecto
        self.filter_buttons[None].setChecked(True)
        
        filters_layout.addStretch()
        main_layout.addWidget(filters_container)
        
        # Área de scroll para las cards mejorada
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 10px;
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.98)};
            }}
            QScrollBar:vertical {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        
        # Widget contenedor de las cards con layout de grid para aprovechar el espacio
        self.orders_container = QWidget()
        self.orders_layout = QGridLayout(self.orders_container)
        # Espaciado entre tarjetas
        spacing = 6 if self.is_small_screen else 10  
        self.orders_layout.setSpacing(spacing)  
        self.orders_layout.setAlignment(Qt.AlignTop)
        margins = 10 if self.is_small_screen else 20
        self.orders_layout.setContentsMargins(margins, margins, margins, margins)
        
        # El número de columnas se calculará dinámicamente en load_orders()
        # según el ancho real de la ventana, no de la pantalla
        self.columns = 1  # Valor inicial
        
        scroll_area.setWidget(self.orders_container)
        main_layout.addWidget(scroll_area)
        
        # Footer con información adicional
        footer_container = QFrame()
        footer_container.setFixedHeight(30)
        footer_container.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
                border-radius: 6px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
            }}
        """)
        footer_layout = QHBoxLayout(footer_container)
        footer_layout.setContentsMargins(8, 4, 8, 4)
        
        self.footer_info = QLabel("Sistema POS - Vista de Cocina")
        footer_font_size = 9 if self.is_small_screen else 10
        self.footer_info.setStyleSheet(f"""
            font-size: {footer_font_size}px;
            color: {ColorPalette.SILVER_LAKE_BLUE};
            font-weight: 500;
        """)
        footer_layout.addWidget(self.footer_info)
        
        footer_layout.addStretch()
        
        # Indicador de conexión
        self.connection_status = QLabel("🟢 Conectado")
        self.connection_status.setStyleSheet(f"""
            font-size: {footer_font_size}px;
            color: {ColorPalette.SUCCESS};
            font-weight: bold;
        """)
        footer_layout.addWidget(self.connection_status)
        
        main_layout.addWidget(footer_container)
        
        # Estilo general mejorado
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.PLATINUM},
                           stop:0.5 {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.98)},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.05)});
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }}
        """)
    
    def filter_orders(self, status):
        """Filtrar pedidos por estado"""
        # Desactivar otros botones
        for btn in self.filter_buttons.values():
            btn.setChecked(False)
        
        # Activar el botón seleccionado
        self.filter_buttons[status].setChecked(True)
        self.current_filter = status
        
        # Forzar actualización de datos desde la base de datos antes de aplicar filtro
        # Esto asegura que siempre tengamos los datos más recientes
        self.order_controller = OrderController()  # Refrescar controlador
        
        # Recargar con filtro
        self.load_orders()
    
    def calculate_columns(self):
        """Calcular número de columnas según el ancho disponible de la ventana"""
        # Obtener el ancho actual de la ventana
        window_width = self.width()
        
        # Determinar tamaño de tarjeta según resolución - SINCRONIZADO con OrderCard
        screen = QApplication.primaryScreen().geometry()
        card_width = 270 if screen.width() <= 1366 else 260  # Usar 260px para ambas resoluciones
        
        # Espaciado y márgenes - REDUCIDOS para permitir más columnas
        spacing = 6 if self.is_small_screen else 10
        margins = 10 if self.is_small_screen else 20
        
        # Calcular ancho disponible restando márgenes, scroll bar y espacios extras
        scroll_bar_width = 15  # Reducido de 20 a 15
        extra_margins = 25     # Reducido de 50 a 25
        
        available_width = window_width - (margins * 2) - scroll_bar_width - extra_margins
        
        # Calcular número de columnas que caben
        columns = max(1, available_width // (card_width + spacing))
        
        # Limitar máximo de columnas para evitar que se vean muy dispersas
        max_columns = 6 if screen.width() > 1366 else 5  # Aumentado a 5 para pantallas pequeñas
        columns = min(columns, max_columns)
        
        return columns
        
    def update_statistics(self, orders):
        """Actualizar estadísticas simplificadas"""
        if not orders:
            self.stats_label.setText("📊 Sin pedidos activos")
            return
        
        pending = sum(1 for order in orders if order.status == OrderStatus.PENDING.value)
        preparing = sum(1 for order in orders if order.status == OrderStatus.PREPARING.value)
        ready = sum(1 for order in orders if order.status == OrderStatus.READY.value)
        delivered = sum(1 for order in orders if order.status == OrderStatus.DELIVERED.value)
        paid = sum(1 for order in orders if order.status == OrderStatus.PAID.value)
        
        # Estadísticas más concisas
        self.stats_label.setText(
            f"Total: {len(orders)} | Pendientes: {pending} | Preparando: {preparing} | Listos: {ready} | Entregados: {delivered} | Pagados: {paid}"
        )

    def update_statistics_summary(self):
        """Actualizar estadísticas en tiempo real"""
        try:
            # Obtener todos los pedidos para estadísticas completas
            all_orders = self.order_controller.get_all_orders_for_kitchen()
            
            # Llamar al método de estadísticas correcto
            self.update_statistics(all_orders)
            
        except Exception as e:
            self.stats_label.setText(f"❌ Error en estadísticas: {str(e)}")

    def load_orders(self):
        """Cargar y mostrar pedidos con filtros actualizados"""
        try:
            # Mostrar indicador de carga
            self.refresh_btn.setText("⏳ Cargando...")
            self.refresh_btn.setEnabled(False)
            
            # Recalcular número de columnas según el ancho actual de la ventana
            self.columns = self.calculate_columns()
            
            # Limpiar layout actual
            for i in reversed(range(self.orders_layout.count())):
                child = self.orders_layout.itemAt(i).widget()
                if child:
                    child.setParent(None)
            
            # Obtener pedidos según el filtro
            if self.current_filter == OrderStatus.PAID:
                # Para pedidos pagados, obtener todos los pedidos para tener acceso a los pagados
                all_orders = self.order_controller.get_all_orders_for_kitchen()
                # Filtrar solo los pagados
                orders = [order for order in all_orders if order.status == OrderStatus.PAID.value]
            elif self.current_filter is None:
                # Para "Todos" mostrar solo pedidos activos (excluyendo pagados)
                orders = self.order_controller.get_active_orders()
            else:
                # Para otros filtros específicos, usar pedidos activos
                all_orders = self.order_controller.get_active_orders()
                # Aplicar filtro
                orders = [order for order in all_orders if order.status == self.current_filter.value]
            
            # Actualizar estadísticas (usar todos los pedidos para estadísticas completas)
            stats_orders = self.order_controller.get_all_orders_for_kitchen()
            self.update_statistics(stats_orders)
            
            # Actualizar tiempo
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if not orders:
                # Mostrar mensaje según filtro
                if self.current_filter is not None:
                    filter_names = {
                        OrderStatus.PENDING: "pendientes",
                        OrderStatus.PREPARING: "en preparación", 
                        OrderStatus.READY: "listos",
                        OrderStatus.DELIVERED: "entregados",
                        OrderStatus.PAID: "pagados"
                    }
                    message = f"🔍 No hay pedidos {filter_names.get(self.current_filter, '')}"
                else:
                    message = "🎉 ¡No hay pedidos pendientes!"
                
                no_orders_label = QLabel(message)
                no_orders_label.setAlignment(Qt.AlignCenter)
                no_orders_label.setStyleSheet(f"""
                    font-size: 18px;
                    color: {ColorPalette.SUCCESS};
                    font-weight: bold;
                    padding: 20px;
                """)
                
                self.orders_layout.addWidget(no_orders_label, 0, 0, 1, self.columns)  # Span across all columns
                self.footer_info.setText(f"🏪 Sistema POS - Sin pedidos activos ({current_time})")
            else:
                # Mostrar pedidos en grid layout aprovechando el espacio horizontal
                # Ordenar por prioridad
                def get_priority(order):
                    elapsed_minutes = (datetime.now() - order.created_at).total_seconds() / 60
                    status_priority = {
                        OrderStatus.DELIVERED: 1,
                        OrderStatus.READY: 2,
                        OrderStatus.PREPARING: 3,
                        OrderStatus.PENDING: 4,
                        OrderStatus.PAID: 5
                    }.get(order.status, 6)
                    
                    # Solo aplicar factor de urgencia para estados activos de cocina
                    if order.status in [OrderStatus.PENDING.value, OrderStatus.PREPARING.value, OrderStatus.READY.value]:
                        urgency_factor = max(0, elapsed_minutes - 10) * 0.1
                    else:
                        # Para entregados y pagados, no aplicar urgencia
                        urgency_factor = 0
                    
                    return (status_priority - urgency_factor, elapsed_minutes)
                
                sorted_orders = sorted(orders, key=get_priority)
                
                # Agregar tarjetas en grid layout
                row, col = 0, 0
                for order in sorted_orders:
                    card = OrderCard(order)
                    
                    # Solo conectar señales si la tarjeta es interactiva (no pagada)
                    if card.is_interactive:
                        card.status_changed.connect(self.update_order_status)
                        card.payment_requested.connect(self.handle_payment_request)
                    
                    self.orders_layout.addWidget(card, row, col)
                    
                    # Avanzar a la siguiente posición
                    col += 1
                    if col >= self.columns:
                        col = 0
                        row += 1
                
                self.footer_info.setText(f"🏪 Sistema POS - {len(orders)} pedidos mostrados ({current_time})")
                
        except Exception as e:
            # Mostrar error
            error_label = QLabel(f"❌ Error al cargar pedidos: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet(f"""
                font-size: 16px;
                color: {ColorPalette.ERROR};
                font-weight: bold;
            """)
            
            self.orders_layout.addWidget(error_label)
            self.connection_status.setText("🔴 Error de conexión")
            self.connection_status.setStyleSheet(f"""
                font-size: 10px;
                color: {ColorPalette.ERROR};
                font-weight: bold;
            """)
        
        finally:
            # Restaurar botón
            self.refresh_btn.setText("🔄 Actualizar")
            self.refresh_btn.setEnabled(True)
    
    def update_order_status(self, order_id, new_status):
        """Actualizar estado de un pedido con mejor feedback"""
        try:
            # Mostrar feedback inmediato
            self.connection_status.setText("🟡 Actualizando...")
            self.connection_status.setStyleSheet(f"""
                font-size: 10px;
                color: {ColorPalette.WARNING};
                font-weight: bold;
            """)
            
            self.order_controller.update_order_status(order_id, new_status)
            self.load_orders()  # Recargar vista
            
            # Feedback de éxito
            self.connection_status.setText("🟢 Conectado")
            self.connection_status.setStyleSheet(f"""
                font-size: 10px;
                color: {ColorPalette.SUCCESS};
                font-weight: bold;
            """)
            
            # Mostrar notificación mejorada
            status_text = {
                OrderStatus.PREPARING: "iniciado",
                OrderStatus.READY: "completado y listo para entregar",
                OrderStatus.DELIVERED: "entregado",
                OrderStatus.CANCELLED: "cancelado"
            }.get(new_status, "actualizado")
            
            # Crear diálogo de confirmación personalizado
            msg = QMessageBox(self)
            msg.setWindowTitle("✅ Estado Actualizado")
            msg.setText(f"Pedido #{order_id} {status_text} correctamente")
            msg.setIcon(QMessageBox.Information)
            
            # Personalizar el estilo del mensaje
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {ColorPalette.PLATINUM};
                    color: {ColorPalette.RICH_BLACK};
                    font-size: 12px;
                }}
                QMessageBox QPushButton {{
                    background-color: {ColorPalette.SUCCESS};
                    color: #ffffff;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                    min-width: 60px;
                }}
                QMessageBox QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
                }}
            """)
            
            # Auto-cerrar después de 2 segundos
            msg.show()
            QTimer.singleShot(2000, msg.close)
            
        except Exception as e:
            # Feedback de error
            self.connection_status.setText("🔴 Error")
            self.connection_status.setStyleSheet(f"""
                font-size: 10px;
                color: {ColorPalette.ERROR};
                font-weight: bold;
            """)
            
            # Diálogo de error personalizado
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("❌ Error")
            error_msg.setText(f"Error al actualizar estado del pedido #{order_id}")
            error_msg.setDetailedText(str(e))
            error_msg.setIcon(QMessageBox.Critical)
            
            error_msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {ColorPalette.PLATINUM};
                    color: {ColorPalette.RICH_BLACK};
                    font-size: 12px;
                }}
                QMessageBox QPushButton {{
                    background-color: {ColorPalette.ERROR};
                    color: #ffffff;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                    min-width: 60px;
                }}
                QMessageBox QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
                }}
            """)
            
            error_msg.exec_()
    
    def handle_payment_request(self, order_id):
        """Manejar solicitud de pago para una orden"""
        try:
            # Obtener detalles de la orden
            order = self.order_controller.get_order_details(order_id)
            if not order:
                QMessageBox.warning(self, "Error", f"No se encontró la orden #{order_id}")
                return
            
            # Importar aquí para evitar importación circular
            from views.pos_window import CustomerInfoDialog
            
            # Crear dialog de pago con información de la orden
            dialog = CustomerInfoDialog(order.total, self, payment_required=True)
            dialog.name_input.setText(order.customer_name)
            if order.table_number:
                dialog.table_input.setValue(order.table_number)
            
            # Cambiar título para indicar que es un pago
            dialog.setWindowTitle(f"Procesar Pago - Orden #{order_id}")
            
            if dialog.exec_() == QDialog.Accepted:
                customer_info = dialog.get_customer_info()
                
                # Procesar el pago
                self.order_controller.complete_payment(order_id, customer_info['payment_method'])
                
                # Actualizar la vista
                self.load_orders()
                
                # Mostrar confirmación
                payment_methods = {
                    'efectivo': '💵 Efectivo',
                    'transferencia': '🏦 Transferencia',
                    'tarjeta': '💳 Tarjeta'
                }
                payment_display = payment_methods.get(customer_info['payment_method'], customer_info['payment_method'])
                
                QMessageBox.information(
                    self, 
                    "✅ Pago Procesado", 
                    f"Pago de la orden #{order_id} procesado exitosamente.\n"
                    f"Cliente: {customer_info['name']}\n"
                    f"Total: ${order.total:.2f}\n"
                    f"Método: {payment_display}"
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar el pago:\n{str(e)}")
    
    def resizeEvent(self, event):
        """Manejar redimensionamiento de la ventana para recalcular columnas"""
        super().resizeEvent(event)
        # Solo recalcular si ya se ha inicializado la vista
        if hasattr(self, 'orders_layout'):
            # Usar un timer para evitar recálculos excesivos durante el redimensionamiento
            if not hasattr(self, 'resize_timer'):
                self.resize_timer = QTimer()
                self.resize_timer.setSingleShot(True)
                self.resize_timer.timeout.connect(self.load_orders)
            
            self.resize_timer.stop()
            self.resize_timer.start(500)  # Esperar 500ms después del último redimensionamiento
    
    def showEvent(self, event):
        """Se ejecuta cuando se muestra la vista - refrescar datos automáticamente"""
        super().showEvent(event)
        # Refrescar datos cada vez que se muestra la vista
        # Solo si ya se ha inicializado completamente
        if hasattr(self, 'order_controller'):
            # Refrescar controlador para obtener datos más recientes
            self.order_controller = OrderController()
            # Recargar los pedidos con el filtro actual
            self.load_orders()

