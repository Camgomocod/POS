from models.base import get_db
from models.order import Order
from models.order_item import OrderItem
from models.product import Product

class OrderController:
    def __init__(self):
        self.db = get_db()
    
    def create_order(self, items):
        """
        items: lista de diccionarios con product_id, quantity
        """
        total = 0
        order_items = []
        
        for item in items:
            product = self.db.query(Product).filter(Product.id == item['product_id']).first()
            if product:
                subtotal = product.price * item['quantity']
                total += subtotal
                
                order_item = OrderItem(
                    product_id=product.id,
                    quantity=item['quantity'],
                    unit_price=product.price,
                    subtotal=subtotal
                )
                order_items.append(order_item)
        
        # Crear orden
        order = Order(total=total)
        self.db.add(order)
        self.db.commit()
        
        # Agregar items
        for item in order_items:
            item.order_id = order.id
            self.db.add(item)
        
        self.db.commit()
        return order
    
    def get_order_details(self, order_id):
        return self.db.query(Order).filter(Order.id == order_id).first()
