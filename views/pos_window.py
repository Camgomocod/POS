# views/pos_window.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from utils.printer import ReceiptPrinter

class POSWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.product_controller = ProductController()
        self.order_controller = OrderController()
        self.printer = ReceiptPrinter()
        self.cart_items = []
        self.init_ui()
        self.load_categories()
        
    def init_ui(self):
        self.setWindowTitle("POS - Restaurante")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        
        # Panel izquierdo - Productos
        left_panel = self.create_product_panel()
        main_layout.addWidget(left_panel, 2)
        
        # Panel derecho - Carrito
        right_panel = self.create_cart_panel()
        main_layout.addWidget(right_panel, 1)
        
    def create_product_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Título
        title = QLabel("MENÚ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Categorías
        self.category_combo = QComboBox()
        self.category_combo.currentTextChanged.connect(self.load_products)
        layout.addWidget(self.category_combo)
        
        # Grid de productos
        scroll = QScrollArea()
        self.products_widget = QWidget()
        self.products_layout = QGridLayout(self.products_widget)
        scroll.setWidget(self.products_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        return panel
    
    def create_cart_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Título
        title = QLabel("ORDEN ACTUAL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Lista del carrito
        self.cart_list = QListWidget()
        layout.addWidget(self.cart_list)
        
        # Total
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        layout.addWidget(self.total_label)
        
        # Botones
        buttons_layout = QVBoxLayout()
        
        clear_btn = QPushButton("Limpiar Carrito")
        clear_btn.clicked.connect(self.clear_cart)
        clear_btn.setStyleSheet("background-color: #ff6b6b; color: white; font-size: 14px; padding: 10px;")
        buttons_layout.addWidget(clear_btn)
        
        pay_btn = QPushButton("PROCESAR PAGO")
        pay_btn.clicked.connect(self.process_payment)
        pay_btn.setStyleSheet("background-color: #51cf66; color: white; font-size: 16px; padding: 15px;")
        buttons_layout.addWidget(pay_btn)
        
        layout.addLayout(buttons_layout)
        
        return panel
    
    def load_categories(self):
        categories = self.product_controller.get_all_categories()
        self.category_combo.addItem("Todas las categorías")
        for category in categories:
            self.category_combo.addItem(category.name, category.id)
    
    def load_products(self):
        # Limpiar productos actuales
        for i in reversed(range(self.products_layout.count())):
            self.products_layout.itemAt(i).widget().setParent(None)
        
        # Obtener productos
        current_text = self.category_combo.currentText()
        if current_text == "Todas las categorías":
            products = self.product_controller.get_all_products()
        else:
            category_id = self.category_combo.currentData()
            products = self.product_controller.get_products_by_category(category_id)
        
        # Mostrar productos en grid
        row, col = 0, 0
        for product in products:
            btn = self.create_product_button(product)
            self.products_layout.addWidget(btn, row, col)
            col += 1
            if col >= 3:  # 3 columnas
                col = 0
                row += 1
    
    def create_product_button(self, product):
        btn = QPushButton()
        btn.setFixedSize(150, 100)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #4dabf7;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #339af0;
            }
        """)
        
        btn.setText(f"{product.name}\n${product.price:.2f}")
        btn.clicked.connect(lambda: self.add_to_cart(product))
        
        return btn
    
    def add_to_cart(self, product):
        # Buscar si el producto ya está en el carrito
        for item in self.cart_items:
            if item['product'].id == product.id:
                item['quantity'] += 1
                break
        else:
            # Agregar nuevo item
            self.cart_items.append({
                'product': product,
                'quantity': 1
            })
        
        self.update_cart_display()
    
    def update_cart_display(self):
        self.cart_list.clear()
        total = 0
        
        for item in self.cart_items:
            product = item['product']
            quantity = item['quantity']
            subtotal = product.price * quantity
            total += subtotal
            
            list_item = QListWidgetItem(f"{product.name} x{quantity} - ${subtotal:.2f}")
            self.cart_list.addItem(list_item)
        
        self.total_label.setText(f"Total: ${total:.2f}")
    
    def clear_cart(self):
        self.cart_items = []
        self.update_cart_display()
    
    def process_payment(self):
        if not self.cart_items:
            QMessageBox.warning(self, "Advertencia", "El carrito está vacío")
            return
        
        # Crear orden
        order_items = []
        for item in self.cart_items:
            order_items.append({
                'product_id': item['product'].id,
                'quantity': item['quantity']
            })
        
        try:
            order = self.order_controller.create_order(order_items)
            
            # Imprimir recibo
            self.printer.print_receipt(order, self.cart_items)
            
            # Limpiar carrito
            self.clear_cart()
            
            QMessageBox.information(self, "Éxito", f"Orden #{order.id} procesada correctamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar la orden: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = POSWindow()
    window.show()
    sys.exit(app.exec_())
