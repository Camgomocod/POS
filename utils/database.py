from models.base import create_tables, get_db
from models.category import Category
from models.product import Product
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.user import User, UserRole
from datetime import datetime, timedelta
import random

def init_database():
    """Inicializar base de datos con datos de ejemplo mejorados"""
    create_tables()
    
    db = get_db()
    
    # Verificar si ya hay datos
    if db.query(Category).count() > 0:
        db.close()
        return
    
    print("  📁 Creando categorías...")
    # Categorías de ejemplo
    categories_data = [
        {"name": "Hamburguesas", "description": "Deliciosas hamburguesas artesanales"},
        {"name": "Bebidas", "description": "Bebidas frías y calientes"},
        {"name": "Acompañamientos", "description": "Papas, ensaladas y más"},
        {"name": "Postres", "description": "Dulces tentaciones"}
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        categories.append(category)
    db.commit()
    
    print("  🍔 Agregando productos al menú...")
    # Productos de ejemplo más completos
    products_data = [
        # Hamburguesas
        {"name": "Clásica", "description": "Carne, lechuga, tomate, cebolla", "price": 8.99, "category_id": 1},
        {"name": "Con Queso", "description": "Clásica + queso cheddar", "price": 9.99, "category_id": 1},
        {"name": "Especial de la Casa", "description": "Doble carne, queso, bacon, salsa especial", "price": 12.99, "category_id": 1},
        {"name": "Pollo Crispy", "description": "Pollo empanizado, lechuga, mayonesa", "price": 10.50, "category_id": 1},
        {"name": "Vegetariana", "description": "Hamburguesa de quinoa y vegetales", "price": 9.50, "category_id": 1},
        
        # Bebidas
        {"name": "Coca Cola", "description": "Refresco clásico 500ml", "price": 2.50, "category_id": 2},
        {"name": "Agua Mineral", "description": "Agua purificada 500ml", "price": 1.50, "category_id": 2},
        {"name": "Jugo Natural", "description": "Jugo de frutas naturales", "price": 3.00, "category_id": 2},
        {"name": "Café Americano", "description": "Café recién preparado", "price": 2.00, "category_id": 2},
        {"name": "Malteada", "description": "Malteada cremosa de vainilla", "price": 4.50, "category_id": 2},
        
        # Acompañamientos
        {"name": "Papas Fritas", "description": "Papas doradas y crujientes", "price": 3.99, "category_id": 3},
        {"name": "Aros de Cebolla", "description": "Aros empanizados y fritos", "price": 4.50, "category_id": 3},
        {"name": "Ensalada César", "description": "Lechuga, crutones, parmesano", "price": 5.99, "category_id": 3},
        {"name": "Nuggets de Pollo", "description": "6 piezas de pollo empanizado", "price": 6.50, "category_id": 3},
        
        # Postres
        {"name": "Helado de Vainilla", "description": "Copa de helado cremoso", "price": 3.50, "category_id": 4},
        {"name": "Torta de Chocolate", "description": "Porción generosa con frosting", "price": 4.99, "category_id": 4},
        {"name": "Brownie", "description": "Brownie tibio con helado", "price": 5.50, "category_id": 4},
        {"name": "Flan Casero", "description": "Flan tradicional con caramelo", "price": 3.99, "category_id": 4}
    ]
    
    products = []
    for prod_data in products_data:
        product = Product(**prod_data)
        db.add(product)
        products.append(product)
    db.commit()
    
    print("  📋 Generando órdenes de ejemplo...")
    # Crear algunas órdenes de ejemplo para el dashboard
    sample_orders_data = [
        # Órdenes de hoy
        {"customer_name": "Juan Pérez", "table_number": 1, "status": OrderStatus.READY},
        {"customer_name": "María García", "table_number": 3, "status": OrderStatus.PREPARING},
        {"customer_name": "Carlos López", "table_number": None, "status": OrderStatus.DELIVERED},
        {"customer_name": "Ana Martínez", "table_number": 5, "status": OrderStatus.PENDING},
        {"customer_name": "Luis Rodríguez", "table_number": 2, "status": OrderStatus.DELIVERED},
    ]
    
    for i, order_data in enumerate(sample_orders_data):
        # Crear orden con tiempo de hoy
        created_time = datetime.now() - timedelta(hours=random.randint(1, 8))
        
        order = Order(
            customer_name=order_data["customer_name"],
            table_number=order_data["table_number"],
            status=order_data["status"],
            created_at=created_time,
            total=0  # Se calculará después
        )
        db.add(order)
        db.commit()
        
        # Agregar items aleatorios a cada orden
        total = 0
        num_items = random.randint(1, 4)
        selected_products = random.sample(products, num_items)
        
        for product in selected_products:
            quantity = random.randint(1, 3)
            subtotal = product.price * quantity
            total += subtotal
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                subtotal=subtotal
            )
            db.add(order_item)
        
        # Actualizar total de la orden
        order.total = total
        db.commit()
    
    print("  👥 Creando usuarios por defecto...")
    # Crear usuarios por defecto
    default_users = [
        {
            "username": "admin",
            "password": "admin123",
            "full_name": "Administrador Principal",
            "email": "admin@restaurantefast.com",
            "role": UserRole.ADMIN
        },
        {
            "username": "usuario",
            "password": "usuario123", 
            "full_name": "Usuario Regular",
            "email": "usuario@restaurantefast.com",
            "role": UserRole.REGULAR
        },
        {
            "username": "cajero",
            "password": "cajero123",
            "full_name": "Cajero Principal",
            "email": "cajero@restaurantefast.com", 
            "role": UserRole.REGULAR
        },
        {
            "username": "gerente",
            "password": "gerente123",
            "full_name": "Gerente de Restaurante",
            "email": "gerente@restaurantefast.com",
            "role": UserRole.ADMIN
        }
    ]
    
    for user_data in default_users:
        user = User(
            username=user_data["username"],
            password=user_data["password"],
            full_name=user_data["full_name"],
            email=user_data["email"],
            role=user_data["role"]
        )
        db.add(user)
    
    db.commit()
    
    db.close()
    print("✅ Base de datos inicializada con datos de ejemplo")