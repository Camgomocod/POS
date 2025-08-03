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
    
    def __init__(self, order):
        super().__init__()
        self.order = order
        self.init_ui()
    
    def init_ui(self):
        # Tamaño responsivo basado en resolución de pantalla - optimizado para aprovechar mejor el espacio
        screen = QApplication.primaryScreen().geometry()
        if screen.width() <= 1366:  # Resoluciones pequeñas (laptops) - 4 columnas
            self.setFixedSize(315, 360)  # Aumentado ancho para aprovechar el 10% de espacio sobrante
            self.font_sizes = {'header': 15, 'customer': 13, 'items': 11, 'status': 13, 'total': 14}
        else:  # Resoluciones más grandes
            self.setFixedSize(320, 420)  # Mantener tamaño para pantallas grandes
            self.font_sizes = {'header': 18, 'customer': 15, 'items': 13, 'status': 15, 'total': 16}
        
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
        
        # Tiempo transcurrido más simple
        elapsed = datetime.now() - self.order.created_at
        minutes = int(elapsed.total_seconds() / 60)
        
        # Determinar color según urgencia
        if minutes > 30:  # Muy urgente
            time_color = ColorPalette.ERROR
            urgency_icon = "🚨"
        elif minutes > 20:  # Urgente
            time_color = ColorPalette.WARNING
            urgency_icon = "⚠️"
        else:
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
        
        # Items del pedido - diseño simple y legible con altura optimizada para 4 columnas
        items_scroll = QScrollArea()
        items_scroll.setWidgetResizable(True)
        items_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        items_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Altura ajustada para resolución 1366x768 con 4 columnas
        items_scroll.setMaximumHeight(140 if screen.width() <= 1366 else 160)  
        items_scroll.setMinimumHeight(120 if screen.width() <= 1366 else 140)  
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
        
        # Botones de acción - simplificados
        if self.order.status != OrderStatus.DELIVERED and self.order.status != OrderStatus.CANCELLED:
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(8)
            
            # Tamaño de botones
            btn_height = 32 if screen.width() <= 1366 else 36
            
            if self.order.status == OrderStatus.PENDING:
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
            
            elif self.order.status == OrderStatus.PREPARING:
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
            
            elif self.order.status == OrderStatus.READY:
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
            
            # Botón cancelar
            if self.order.status != OrderStatus.DELIVERED:
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
        
        # Indicador de última actualización simplificado
        self.last_update_label = QLabel("Última actualización: --:--")
        self.last_update_label.setStyleSheet(f"""
            font-size: {btn_font_size - 1}px;
            color: {ColorPalette.SILVER_LAKE_BLUE};
            padding: 4px 8px;
            background-color: {ColorPalette.PLATINUM};
            border-radius: 4px;
        """)
        controls_layout.addWidget(self.last_update_label)
        
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
            ("Listos", OrderStatus.READY, ColorPalette.SUCCESS)
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
        
        # Widget contenedor de las cards con espaciado optimizado para tarjetas más grandes
        self.orders_container = QWidget()
        self.orders_layout = QGridLayout(self.orders_container)
        # Espaciado ajustado para las tarjetas de 305px de ancho
        spacing = 8 if self.is_small_screen else 8  
        self.orders_layout.setSpacing(spacing)  
        self.orders_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        margins = 10 if self.is_small_screen else 10
        self.orders_layout.setContentsMargins(margins, margins, margins, margins)
        
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
        
        # Recargar con filtro
        self.load_orders()
        
    def update_statistics(self, orders):
        """Actualizar estadísticas simplificadas"""
        if not orders:
            self.stats_label.setText("📊 Sin pedidos activos")
            return
        
        pending = sum(1 for order in orders if order.status == OrderStatus.PENDING)
        preparing = sum(1 for order in orders if order.status == OrderStatus.PREPARING)
        ready = sum(1 for order in orders if order.status == OrderStatus.READY)
        
        # Estadísticas más concisas
        self.stats_label.setText(
            f"Total: {len(orders)} | Pendientes: {pending} | Preparando: {preparing} | Listos: {ready}"
        )
    
    def load_orders(self):
        """Cargar y mostrar pedidos activos con mejoras visuales"""
        # Actualizar indicador de carga
        self.refresh_btn.setText("🔄 Cargando...")
        self.refresh_btn.setEnabled(False)
        
        # Limpiar cards existentes
        for i in reversed(range(self.orders_layout.count())):
            child = self.orders_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Obtener pedidos activos
        try:
            all_orders = self.order_controller.get_active_orders()
            
            # Aplicar filtro si está activo
            if self.current_filter is not None:
                orders = [order for order in all_orders if order.status == self.current_filter]
            else:
                orders = all_orders
            
            # Actualizar estadísticas
            self.update_statistics(all_orders)
            
            # Actualizar información del footer
            current_time = datetime.now().strftime("%H:%M:%S")
            self.last_update_label.setText(f"Última actualización: {current_time}")
            
            if not orders:
                # Mostrar mensaje apropiado según el filtro
                if self.current_filter is not None:
                    filter_names = {
                        OrderStatus.PENDING: "pendientes",
                        OrderStatus.PREPARING: "en preparación",
                        OrderStatus.READY: "listos"
                    }
                    message = f"🔍 No hay pedidos {filter_names.get(self.current_filter, '')}"
                else:
                    message = "🎉 ¡No hay pedidos pendientes!"
                
                no_orders_container = QFrame()
                no_orders_container.setStyleSheet(f"""
                    QFrame {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                   stop:0 {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.1)},
                                   stop:1 {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)});
                        border-radius: 12px;
                        border: 3px dashed {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.4)};
                        padding: 60px;
                    }}
                """)
                no_orders_layout = QVBoxLayout(no_orders_container)
                
                no_orders_label = QLabel(message)
                no_orders_label.setAlignment(Qt.AlignCenter)
                font_size = 20 if self.is_small_screen else 24
                no_orders_label.setStyleSheet(f"""
                    font-size: {font_size}px;
                    color: {ColorPalette.SUCCESS};
                    font-weight: bold;
                    padding: 20px;
                """)
                no_orders_layout.addWidget(no_orders_label)
                
                # Sugerencia según el filtro
                if self.current_filter is not None:
                    suggestion = QLabel("💡 Prueba cambiar el filtro para ver otros pedidos")
                    suggestion.setAlignment(Qt.AlignCenter)
                    suggestion.setStyleSheet(f"""
                        font-size: {font_size - 6}px;
                        color: {ColorPalette.SILVER_LAKE_BLUE};
                        font-style: italic;
                        padding: 10px 0px 0px 0px;
                    """)
                    no_orders_layout.addWidget(suggestion)
                
                self.orders_layout.addWidget(no_orders_container, 0, 0, 1, -1)
                self.footer_info.setText(f"🏪 Sistema POS - Sin pedidos activos ({current_time})")
            else:
                # Mostrar pedidos en grid responsivo optimizado
                screen_width = QApplication.primaryScreen().geometry().width()
                if screen_width <= 1366:  # Laptop pequeño - 4 columnas para mejor aprovechamiento
                    max_cols = 4  # Aumentado de 3 a 4 para aprovechar el espacio disponible
                elif screen_width <= 1920:  # Laptop/Desktop estándar
                    max_cols = 4
                else:  # Pantallas grandes
                    max_cols = 5
                
                row, col = 0, 0
                
                # Ordenar por prioridad: urgencia -> estado -> tiempo
                def get_priority(order):
                    elapsed_minutes = (datetime.now() - order.created_at).total_seconds() / 60
                    status_priority = {
                        OrderStatus.READY: 1,      # Más prioritario
                        OrderStatus.PREPARING: 2,
                        OrderStatus.PENDING: 3    # Menos prioritario
                    }.get(order.status, 4)
                    
                    urgency_factor = max(0, elapsed_minutes - 10) * 0.1  # Factor de urgencia
                    return (status_priority - urgency_factor, elapsed_minutes)
                
                sorted_orders = sorted(orders, key=get_priority)
                
                for order in sorted_orders:
                    card = OrderCard(order)
                    card.status_changed.connect(self.update_order_status)
                    
                    self.orders_layout.addWidget(card, row, col)
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                
                self.footer_info.setText(f"🏪 Sistema POS - {len(orders)} pedidos mostrados ({current_time})")
                
        except Exception as e:
            # Manejar errores de conexión
            error_container = QFrame()
            error_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.1)};
                    border-radius: 12px;
                    border: 3px solid {ColorPalette.ERROR};
                    padding: 50px;
                }}
            """)
            error_layout = QVBoxLayout(error_container)
            
            error_label = QLabel(f"❌ Error al cargar pedidos: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet(f"""
                font-size: 16px;
                color: {ColorPalette.ERROR};
                font-weight: bold;
            """)
            error_layout.addWidget(error_label)
            
            self.orders_layout.addWidget(error_container, 0, 0)
            self.connection_status.setText("🔴 Error de conexión")
            self.connection_status.setStyleSheet(f"""
                font-size: 10px;
                color: {ColorPalette.ERROR};
                font-weight: bold;
            """)
        
        finally:
            # Restaurar botón de actualizar
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

