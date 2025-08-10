from models.base import get_db
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.product import Product
from datetime import datetime

class OrderController:
    def __init__(self):
        self.db = get_db()
    
    def create_order(self, items, customer_name="Cliente", table_number=None):
        """Crear orden con información del cliente"""
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
        order = Order(
            total=total,
            customer_name=customer_name,
            table_number=table_number,
            status=OrderStatus.PENDING.value
        )
        self.db.add(order)
        self.db.commit()
        
        # Agregar items
        for item in order_items:
            item.order_id = order.id
            self.db.add(item)
        
        self.db.commit()
        return order
    
    def update_order_status(self, order_id, new_status):
        """Actualizar estado del pedido"""
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            # Asegurar que se use el valor string del enum
            if hasattr(new_status, 'value'):
                order.status = new_status.value
            else:
                order.status = new_status
            order.updated_at = datetime.now()
            self.db.commit()
            return order
        return None
    
    def get_orders_by_status(self, status):
        """Obtener pedidos por estado"""
        return self.db.query(Order).filter(Order.status == status).all()
    
    def get_active_orders(self):
        """Obtener pedidos activos (no pagados ni cancelados)"""
        return self.db.query(Order).filter(
            Order.status.in_([OrderStatus.PENDING.value, OrderStatus.PREPARING.value, OrderStatus.READY.value, OrderStatus.DELIVERED.value])
        ).order_by(Order.created_at.asc()).all()
    
    def get_all_orders_for_kitchen(self):
        """Obtener todos los pedidos para la vista de cocina (incluyendo pagados de los últimos días)"""
        from datetime import date, timedelta, datetime
        today = date.today()
        # Incluir pedidos de los últimos 3 días para mostrar pagados recientes
        start_date = today - timedelta(days=3)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        
        return self.db.query(Order).filter(
            Order.status.in_([
                OrderStatus.PENDING.value, OrderStatus.PREPARING.value, OrderStatus.READY.value, 
                OrderStatus.DELIVERED.value, OrderStatus.PAID.value
            ]),
            Order.created_at >= start_datetime  # Últimos 3 días
        ).order_by(Order.created_at.desc()).all()  # Más recientes primero
    
    def get_order_details(self, order_id):
        """Obtener detalles completos del pedido"""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def complete_payment(self, order_id, payment_method="efectivo"):
        """Marcar orden como pagada"""
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            # Marcar como PAID para que aparezca en historial de pagos
            order.status = OrderStatus.PAID.value
            order.payment_method = payment_method
            order.updated_at = datetime.now()
            self.db.commit()
            return order
        return None