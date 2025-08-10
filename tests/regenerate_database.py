"""
Script para regenerar la base de datos con datos sintéticos limpios
Respeta todas las correcciones aplicadas y el diseño actual de modelos
"""
import os
import sys
import sqlite3
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.base import get_db, engine, Base
from models.user import User, UserRole
from models.category import Category
from models.product import Product
from models.order import Order, OrderStatus
from models.order_item import OrderItem

def delete_existing_database():
    """Eliminar base de datos existente si existe"""
    db_path = "data/pos.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Base de datos anterior eliminada")
    
    # También eliminar archivos relacionados
    for file in ["data/pos.db-shm", "data/pos.db-wal", "data/pos_backup.db"]:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Archivo {file} eliminado")

def create_fresh_database():
    """Crear estructura de base de datos limpia"""
    print("🏗️ Creando estructura de base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Estructura de base de datos creada")

def create_users():
    """Crear usuarios del sistema"""
    print("👥 Creando usuarios...")
    db = get_db()
    
    users = [
        User(
            username="admin",
            password="admin123",
            full_name="Administrador Principal",
            email="admin@pos.com",
            role=UserRole.ADMIN
        ),
        User(
            username="cajero1",
            password="cajero123",
            full_name="María González",
            email="maria@pos.com",
            role=UserRole.REGULAR
        ),
        User(
            username="cajero2",
            password="cajero123",
            full_name="Carlos Martínez",
            email="carlos@pos.com",
            role=UserRole.REGULAR
        )
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()
    print(f"✅ {len(users)} usuarios creados")
    return users

def create_categories():
    """Crear categorías de productos"""
    print("📂 Creando categorías...")
    db = get_db()
    
    categories = [
        Category(name="Bebidas", description="Bebidas frías y calientes"),
        Category(name="Comida Rápida", description="Hamburguesas, hot dogs, etc."),
        Category(name="Postres", description="Dulces y postres"),
        Category(name="Ensaladas", description="Ensaladas frescas"),
        Category(name="Café", description="Café y bebidas calientes"),
        Category(name="Snacks", description="Aperitivos y bocadillos")
    ]
    
    for category in categories:
        db.add(category)
    
    db.commit()
    print(f"✅ {len(categories)} categorías creadas")
    return categories

def create_products(categories):
    """Crear productos por categoría"""
    print("🍔 Creando productos...")
    db = get_db()
    
    # Refrescar categorías en la sesión actual
    categories = db.query(Category).all()
    
    products_data = {
        "Bebidas": [
            ("Coca Cola", "Refresco de cola 350ml", 2.50, 1.20),
            ("Pepsi", "Refresco de cola 350ml", 2.50, 1.20),
            ("Sprite", "Refresco de limón 350ml", 2.50, 1.20),
            ("Agua Mineral", "Agua embotellada 500ml", 1.50, 0.80),
            ("Jugo de Naranja", "Jugo natural de naranja 250ml", 3.00, 1.50),
            ("Té Helado", "Té frío con limón 400ml", 2.80, 1.40)
        ],
        "Comida Rápida": [
            ("Hamburguesa Clásica", "Carne, lechuga, tomate, cebolla", 8.50, 4.20),
            ("Hamburguesa Doble", "Doble carne con queso", 12.00, 6.00),
            ("Hot Dog", "Salchicha con mostaza y ketchup", 5.50, 2.80),
            ("Papas Fritas", "Papas fritas medianas", 4.00, 2.00),
            ("Nuggets de Pollo", "8 piezas con salsa", 7.50, 3.80),
            ("Sandwich Club", "Pollo, tocino, lechuga, tomate", 9.00, 4.50)
        ],
        "Postres": [
            ("Helado de Vainilla", "Copa de helado con topping", 4.50, 2.20),
            ("Brownie", "Brownie de chocolate caliente", 5.00, 2.50),
            ("Cheesecake", "Rebanada de cheesecake", 6.00, 3.00),
            ("Flan", "Flan casero con caramelo", 4.00, 2.00),
            ("Tiramisú", "Postre italiano", 7.00, 3.50),
            ("Sundae", "Helado con frutas y crema", 5.50, 2.80)
        ],
        "Ensaladas": [
            ("Ensalada César", "Lechuga, pollo, crutones, aderezo", 7.50, 3.80),
            ("Ensalada Griega", "Tomate, pepino, queso feta, aceitunas", 6.50, 3.20),
            ("Ensalada Mixta", "Lechuga, tomate, zanahoria, maíz", 5.50, 2.80),
            ("Ensalada de Atún", "Atún, lechuga, huevo, tomate", 8.00, 4.00)
        ],
        "Café": [
            ("Café Americano", "Café negro tradicional", 2.00, 0.80),
            ("Café con Leche", "Café con leche vaporizada", 2.80, 1.20),
            ("Cappuccino", "Café con leche espumosa", 3.50, 1.60),
            ("Latte", "Café con mucha leche", 4.00, 1.80),
            ("Espresso", "Café concentrado", 2.50, 1.00),
            ("Mocha", "Café con chocolate", 4.50, 2.00)
        ],
        "Snacks": [
            ("Nachos", "Chips con queso derretido", 5.00, 2.50),
            ("Alitas de Pollo", "6 alitas picantes", 8.00, 4.00),
            ("Quesadilla", "Tortilla con queso", 6.00, 3.00),
            ("Empanadas", "2 empanadas de carne", 4.50, 2.20),
            ("Tequeños", "6 tequeños con queso", 5.50, 2.80)
        ]
    }
    
    products = []
    for category in categories:
        if category.name in products_data:
            for name, desc, price, cost in products_data[category.name]:
                product = Product(
                    name=name,
                    description=desc,
                    price=Decimal(str(price)),
                    cost=Decimal(str(cost)),
                    category_id=category.id,
                    is_active=True,
                    stock=random.randint(50, 200)
                )
                products.append(product)
                db.add(product)
    
    db.commit()
    print(f"✅ {len(products)} productos creados")
    return products

def create_sample_orders(products):
    """Crear órdenes de ejemplo con diferentes estados"""
    print("🧾 Creando órdenes de ejemplo...")
    db = get_db()
    
    # Refrescar productos en la sesión actual
    products = db.query(Product).all()
    
    # Nombres de clientes ejemplo
    customers = [
        "Juan Pérez", "María García", "Carlos López", "Ana Martínez",
        "Luis Rodríguez", "Carmen Sánchez", "Miguel Torres", "Laura Ruiz",
        "Fernando Castro", "Isabel Moreno", "Roberto Silva", "Patricia Díaz",
        "Andrés Herrera", "Rosa Jiménez", "Manuel Vargas", "Elena Ramos"
    ]
    
    orders = []
    
    # Crear órdenes de los últimos 7 días
    for day_offset in range(7):
        base_date = datetime.now() - timedelta(days=day_offset)
        
        # Número de órdenes por día (más recientes tienen más)
        orders_per_day = random.randint(8, 15) if day_offset < 2 else random.randint(3, 8)
        
        for _ in range(orders_per_day):
            # Hora aleatoria del día
            hour = random.randint(8, 22)
            minute = random.randint(0, 59)
            order_time = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Estado basado en la antigüedad de la orden
            if day_offset == 0:  # Hoy
                status_weights = [
                    (OrderStatus.PENDING.value, 0.1),
                    (OrderStatus.PREPARING.value, 0.2),
                    (OrderStatus.READY.value, 0.1),
                    (OrderStatus.DELIVERED.value, 0.3),
                    (OrderStatus.PAID.value, 0.3)
                ]
            elif day_offset <= 2:  # Últimos 2 días
                status_weights = [
                    (OrderStatus.DELIVERED.value, 0.2),
                    (OrderStatus.PAID.value, 0.8)
                ]
            else:  # Días anteriores - mayoría pagadas
                status_weights = [
                    (OrderStatus.DELIVERED.value, 0.1),
                    (OrderStatus.PAID.value, 0.9)
                ]
            
            # Seleccionar estado basado en pesos
            status = random.choices(
                [s[0] for s in status_weights],
                weights=[s[1] for s in status_weights]
            )[0]
            
            # Crear orden
            order = Order(
                customer_name=random.choice(customers),
                table_number=random.choice([None, None, random.randint(1, 20)]),  # 2/3 para llevar
                status=status,
                created_at=order_time,
                updated_at=order_time + timedelta(minutes=random.randint(5, 45)),
                payment_method=random.choice(["efectivo", "tarjeta", "transferencia"]) if status == OrderStatus.PAID.value else None
            )
            
            # Agregar items a la orden (1-4 productos)
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, num_items)
            order_total = 0
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                unit_price = float(product.price)
                subtotal = quantity * unit_price
                order_total += subtotal
                
                order_item = OrderItem(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )
                order.items.append(order_item)
            
            order.total = order_total
            orders.append(order)
            db.add(order)
    
    db.commit()
    print(f"✅ {len(orders)} órdenes creadas")
    
    # Estadísticas por estado
    status_counts = {}
    for order in orders:
        status_counts[order.status] = status_counts.get(order.status, 0) + 1
    
    print("📊 Estadísticas de órdenes:")
    for status, count in status_counts.items():
        print(f"   {status}: {count} órdenes")
    
    return orders

def verify_data_integrity():
    """Verificar integridad de los datos creados"""
    print("🔍 Verificando integridad de datos...")
    db = get_db()
    
    # Verificar usuarios
    users = db.query(User).all()
    print(f"✅ Usuarios: {len(users)}")
    for user in users:
        print(f"   - {user.username} ({user.role.value}) - {user.full_name}")
    
    # Verificar categorías y productos
    categories = db.query(Category).all()
    print(f"✅ Categorías: {len(categories)}")
    for category in categories:
        product_count = db.query(Product).filter(Product.category_id == category.id).count()
        print(f"   - {category.name}: {product_count} productos")
    
    # Verificar órdenes
    orders = db.query(Order).all()
    print(f"✅ Órdenes totales: {len(orders)}")
    
    # Verificar por estado usando los valores string correctos
    for status in OrderStatus:
        count = db.query(Order).filter(Order.status == status.value).count()
        print(f"   - {status.name}: {count} órdenes")
    
    # Verificar órdenes pagadas para payment_history
    paid_orders = db.query(Order).filter(Order.status == OrderStatus.PAID.value).all()
    print(f"✅ Órdenes pagadas (para historial): {len(paid_orders)}")
    
    # Verificar órdenes para cocina (últimos 3 días)
    from datetime import date
    start_date = date.today() - timedelta(days=3)
    start_datetime = datetime.combine(start_date, datetime.min.time())
    kitchen_orders = db.query(Order).filter(
        Order.status.in_([
            OrderStatus.PENDING.value, OrderStatus.PREPARING.value, 
            OrderStatus.READY.value, OrderStatus.DELIVERED.value, 
            OrderStatus.PAID.value
        ]),
        Order.created_at >= start_datetime
    ).all()
    print(f"✅ Órdenes para cocina (últimos 3 días): {len(kitchen_orders)}")

def main():
    """Función principal para regenerar la base de datos"""
    print("🚀 REGENERANDO BASE DE DATOS CON DATOS SINTÉTICOS")
    print("=" * 50)
    
    try:
        # Paso 1: Eliminar base de datos existente
        delete_existing_database()
        
        # Paso 2: Crear estructura limpia
        create_fresh_database()
        
        # Paso 3: Crear datos base
        users = create_users()
        categories = create_categories()
        products = create_products(None)  # No necesita parámetro
        orders = create_sample_orders(None)  # No necesita parámetro
        
        # Paso 4: Verificar integridad
        verify_data_integrity()
        
        print("=" * 50)
        print("✅ BASE DE DATOS REGENERADA EXITOSAMENTE")
        print("\nCredenciales de acceso:")
        print("👤 Admin: usuario='admin', contraseña='admin123'")
        print("👤 Cajero1: usuario='cajero1', contraseña='cajero123'")
        print("👤 Cajero2: usuario='cajero2', contraseña='cajero123'")
        print("\nLa base de datos contiene:")
        print("- Usuarios con roles correctos")
        print("- Categorías y productos variados")
        print("- Órdenes de los últimos 7 días con estados realistas")
        print("- Datos compatible con todas las correcciones aplicadas")
        
    except Exception as e:
        print(f"❌ Error durante la regeneración: {e}")
        raise

if __name__ == "__main__":
    main()
