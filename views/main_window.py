# views/main_window.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from views.pos_window import EnhancedPOSWindow
from views.kitchen_orders_window import KitchenOrdersWindow
from controllers.report_controller import ReportController

class DashboardCard(QFrame):
    """Card informativo para el dashboard"""
    
    def __init__(self, title, value, icon, color):
        super().__init__()
        self.init_ui(title, value, icon, color)
    
    def init_ui(self, title, value, icon, color):
        self.setFixedSize(250, 120)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {color}dd);
                border-radius: 15px;
                color: #ffffff;
            }}
            QFrame:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}ee, stop:1 {color}cc);
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Contenido de texto
        text_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(255,255,255,0.9);")
        text_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        text_layout.addWidget(value_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 36px;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

class MainWindow(QMainWindow):
    """Ventana principal con navegación y dashboard"""
    
    def __init__(self):
        super().__init__()
        self.report_controller = ReportController()
        self.pos_window = None
        self.kitchen_window = None
        self.init_ui()
        self.load_dashboard_data()
    
    def init_ui(self):
        self.setWindowTitle("🍔 Sistema POS - RestauranteFast")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # Header
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Dashboard cards
        dashboard_layout = self.create_dashboard()
        main_layout.addWidget(dashboard_layout)
        
        # Botones principales
        buttons_layout = self.create_main_buttons()
        main_layout.addLayout(buttons_layout)
        
        main_layout.addStretch()
        
        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
    
    def create_header(self):
        """Crear header de la aplicación"""
        layout = QHBoxLayout()
        
        # Logo y título
        title_layout = QVBoxLayout()
        
        title = QLabel("🍔 SISTEMA POS")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("RestauranteFast - Panel de Control")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: rgba(255,255,255,0.8);
        """)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Botón actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: #ffffff;
                border: 2px solid rgba(255,255,255,0.3);
                padding: 10px 20px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
                border: 2px solid rgba(255,255,255,0.5);
            }
        """)
        refresh_btn.clicked.connect(self.load_dashboard_data)
        layout.addWidget(refresh_btn)
        
        return layout
    
    def create_dashboard(self):
        """Crear cards del dashboard"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,0.1);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(container)
        
        # Título del dashboard
        dashboard_title = QLabel("📊 Resumen del Día")
        dashboard_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
        """)
        layout.addWidget(dashboard_title)
        
        # Grid de cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        
        # Cards informativos (se actualizarán dinámicamente)
        self.sales_card = DashboardCard("Ventas del Día", "$0.00", "💰", "#00b894")
        self.orders_card = DashboardCard("Pedidos Hoy", "0", "📋", "#74b9ff")
        self.pending_card = DashboardCard("Pedidos Pendientes", "0", "⏰", "#fdcb6e")
        self.ready_card = DashboardCard("Listos para Entregar", "0", "✅", "#55a3ff")
        
        cards_layout.addWidget(self.sales_card, 0, 0)
        cards_layout.addWidget(self.orders_card, 0, 1)
        cards_layout.addWidget(self.pending_card, 1, 0)
        cards_layout.addWidget(self.ready_card, 1, 1)
        
        layout.addLayout(cards_layout)
        
        return container
    
    def create_main_buttons(self):
        """Crear botones principales de navegación"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Botón POS
        pos_btn = self.create_nav_button(
            "💳 PUNTO DE VENTA",
            "Procesar pedidos y ventas",
            "#e17055",
            self.open_pos
        )
        layout.addWidget(pos_btn)
        
        # Botón Cocina
        kitchen_btn = self.create_nav_button(
            "👨‍🍳 COCINA",
            "Gestionar estado de pedidos",
            "#00b894",
            self.open_kitchen
        )
        layout.addWidget(kitchen_btn)
        
        # Botón Reportes (futuro)
        reports_btn = self.create_nav_button(
            "📊 REPORTES",
            "Ver estadísticas y reportes",
            "#6c5ce7",
            self.show_coming_soon
        )
        layout.addWidget(reports_btn)
        
        return layout
    
    def create_nav_button(self, title, description, color, callback):
        """Crear botón de navegación estilizado"""
        btn = QPushButton()
        btn.setFixedSize(350, 100)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {color}dd);
                color: #ffffff;
                border: none;
                border-radius: 15px;
                padding: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}ee, stop:1 {color}cc);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}aa, stop:1 {color}88);
            }}
        """)
        
        # Layout interno
        layout = QVBoxLayout(btn)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.9);")
        layout.addWidget(desc_label)
        
        btn.clicked.connect(callback)
        
        return btn
    
    def load_dashboard_data(self):
        """Cargar datos del dashboard"""
        try:
            # Ventas del día
            daily_sales = self.report_controller.get_daily_sales()
            self.sales_card.findChild(QLabel).setText(f"${daily_sales:.2f}")
            
            # Pedidos recientes para contar
            recent_orders = self.report_controller.get_recent_orders(50)  # Últimas 50 órdenes
            today_orders = [o for o in recent_orders if o.created_at.date() == datetime.now().date()]
            self.orders_card.findChild(QLabel).setText(str(len(today_orders)))
            
            # Pedidos por estado
            from models.order import OrderStatus
            pending_orders = self.report_controller.db.query(Order).filter(
                Order.status.in_([OrderStatus.PENDING, OrderStatus.PREPARING])
            ).count()
            
            ready_orders = self.report_controller.db.query(Order).filter(
                Order.status == OrderStatus.READY
            ).count()
            
            # Actualizar cards
            for card in [self.pending_card, self.ready_card]:
                for label in card.findChildren(QLabel):
                    if "Pendientes" in card.findChild(QLabel).text():
                        if "0" in label.text() or "$" not in label.text():
                            label.setText(str(pending_orders))
                            break
                    elif "Entregar" in card.findChild(QLabel).text():
                        if "0" in label.text() or "$" not in label.text():
                            label.setText(str(ready_orders))
                            break
            
        except Exception as e:
            print(f"Error cargando dashboard: {e}")
    
    def open_pos(self):
        """Abrir ventana POS"""
        if not self.pos_window:
            self.pos_window = EnhancedPOSWindow()
        else:
            # Si ya existe, refrescar datos
            if hasattr(self.pos_window, 'refresh_data'):
                self.pos_window.refresh_data()
        self.pos_window.show()
        self.pos_window.raise_()
    
    def open_kitchen(self):
        """Abrir ventana de cocina"""
        if not self.kitchen_window:
            self.kitchen_window = KitchenOrdersWindow()
        else:
            # Si ya existe, refrescar datos forzando nueva instancia del controlador
            if hasattr(self.kitchen_window, 'order_controller'):
                from controllers.order_controller import OrderController
                self.kitchen_window.order_controller = OrderController()
                if hasattr(self.kitchen_window, 'load_orders'):
                    self.kitchen_window.load_orders()
        self.kitchen_window.show()
        self.kitchen_window.raise_()
    
    def show_coming_soon(self):
        """Mostrar mensaje de próximamente"""
        QMessageBox.information(
            self,
            "Próximamente",
            "🚧 Esta funcionalidad estará disponible pronto.\n\nIncluirá:\n• Reportes de ventas\n• Gráficos estadísticos\n• Análisis de productos\n• Historial detallado"
        )

if __name__ == '__main__':
    from datetime import datetime
    from models.order import Order
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())