#!/usr/bin/env python3
"""
Script para generar una base de datos con datos de prueba
para testing de reportes y gráficas
"""

import os
import sys
import shutil
from datetime import datetime, timedelta
from decimal import Decimal
from random import randint, choice, uniform
from faker import Faker

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.base import Base, engine, create_tables, get_db
from models.category import Category
from models.product import Product
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.user import User, UserRole
from sqlalchemy import func

# Configurar Faker en español
fake = Faker('es_ES')

class TestDataGenerator:
    """Generador de datos de prueba"""
    
    def __init__(self):
        self.db = get_db()
        
    def backup_current_database(self):
        """Crear backup de la base de datos actual"""
        try:
            current_db = "data/pos.db"
            backup_db = f"data/pos_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            if os.path.exists(current_db):
                shutil.copy2(current_db, backup_db)
                print(f"✅ Backup creado: {backup_db}")
            else:
                print("ℹ️  No existe base de datos actual para hacer backup")
                
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
    
    def create_test_database(self):
        """Crear nueva base de datos con datos de prueba"""
        try:
            # Crear backup primero
            self.backup_current_database()
            
            # Eliminar base de datos actual si existe
            if os.path.exists("data/pos.db"):
                os.remove("data/pos.db")
                print("🗑️  Base de datos anterior eliminada")
            
            # Crear nuevas tablas
            create_tables()
            print("📊 Nuevas tablas creadas")
            
            # Generar datos
            self.create_categories()
            self.create_products()
            self.generate_users()
            self.create_historical_orders()
            
            print("🎉 Base de datos de prueba generada exitosamente!")
            print("📈 Datos disponibles para testing de reportes y gráficas")
            
        except Exception as e:
            print(f"❌ Error generando base de datos: {e}")
            self.db.rollback()
    
    def create_categories(self):
        """Crear categorías de prueba"""
        categories_data = [
            ("🍔 Hamburguesas", "Deliciosas hamburguesas artesanales"),
            ("🍕 Pizzas", "Pizzas tradicionales e innovadoras"),
            ("🍗 Pollo", "Especialidades en pollo frito y asado"),
            ("🥗 Ensaladas", "Ensaladas frescas y saludables"),
            ("🍟 Acompañamientos", "Papas, aros de cebolla y más"),
            ("🥤 Bebidas", "Refrescos, jugos y bebidas calientes"),
            ("🍰 Postres", "Dulces tentaciones para cerrar con broche de oro"),
            ("🌮 Mexicana", "Sabores auténticos de México"),
            ("🍝 Pasta", "Pastas frescas y salsas caseras"),
            ("🥪 Sándwiches", "Sándwiches gourmet y wraps"),
        ]
        
        for name, description in categories_data:
            category = Category(name=name, description=description, is_active=True)
            self.db.add(category)
        
        self.db.commit()
        print(f"✅ {len(categories_data)} categorías creadas")
    
    def create_products(self):
        """Crear productos de prueba"""
        categories = self.db.query(Category).all()
        
        products_by_category = {
            "🍔 Hamburguesas": [
                ("Hamburguesa Clásica", "Carne de res, lechuga, tomate, cebolla y salsa especial", 15000, 7000, 25, 50),
                ("Hamburguesa BBQ", "Carne de res, bacon, queso cheddar, cebolla crispy y salsa BBQ", 18000, 8500, 30, 45),
                ("Hamburguesa Vegetariana", "Hamburguesa de lentejas, aguacate, lechuga y tomate", 14000, 6000, 20, 30),
                ("Hamburguesa Doble", "Doble carne, doble queso, bacon y papas", 22000, 10000, 35, 60),
                ("Hamburguesa Picante", "Carne especiada, jalapeños, queso pepper jack", 17000, 8000, 25, 40),
            ],
            "🍕 Pizzas": [
                ("Pizza Margherita", "Salsa de tomate, mozzarella fresca y albahaca", 16000, 7500, 20, 35),
                ("Pizza Pepperoni", "Salsa de tomate, mozzarella y pepperoni", 18000, 8500, 25, 40),
                ("Pizza Cuatro Quesos", "Mozzarella, gorgonzola, parmesano y provolone", 20000, 9500, 30, 45),
                ("Pizza Hawaiana", "Jamón, piña, mozzarella y salsa de tomate", 17000, 8000, 25, 40),
                ("Pizza Vegetariana", "Pimientos, champiñones, cebolla, aceitunas", 19000, 9000, 30, 50),
            ],
            "🍗 Pollo": [
                ("Pollo Frito Original", "8 piezas de pollo frito con especias secretas", 24000, 12000, 45, 80),
                ("Alitas BBQ", "12 alitas bañadas en salsa BBQ", 16000, 7500, 25, 35),
                ("Pollo a la Plancha", "Pechuga de pollo con hierbas y limón", 15000, 7000, 20, 30),
                ("Nuggets de Pollo", "10 nuggets crujientes con salsas", 12000, 5500, 15, 25),
                ("Pollo Teriyaki", "Muslos de pollo glaseados en salsa teriyaki", 17000, 8000, 30, 40),
            ],
            "🥗 Ensaladas": [
                ("Ensalada César", "Lechuga romana, crutones, parmesano y aderezo césar", 12000, 5000, 10, 20),
                ("Ensalada Griega", "Tomate, pepino, aceitunas, queso feta", 14000, 6000, 15, 25),
                ("Ensalada de Pollo", "Mix de lechugas, pollo a la plancha, aguacate", 16000, 7500, 20, 30),
                ("Ensalada Caprese", "Tomate, mozzarella, albahaca y aceite de oliva", 13000, 5500, 10, 20),
            ],
            "🍟 Acompañamientos": [
                ("Papas Fritas", "Papas cortadas y fritas al punto perfecto", 6000, 2500, 10, 15),
                ("Aros de Cebolla", "Aros de cebolla empanizados y fritos", 7000, 3000, 12, 20),
                ("Papas con Queso", "Papas fritas cubiertas con queso derretido", 8000, 3500, 15, 25),
                ("Bastones de Mozzarella", "Queso mozzarella empanizado", 9000, 4000, 15, 20),
            ],
            "🥤 Bebidas": [
                ("Coca Cola", "Bebida gaseosa clásica 350ml", 3000, 1200, 0, 0),
                ("Jugo Natural", "Jugo de frutas frescas 400ml", 4000, 1800, 5, 10),
                ("Agua Mineral", "Agua mineral 500ml", 2500, 1000, 0, 0),
                ("Café Americano", "Café colombiano premium", 3500, 1500, 3, 8),
                ("Limonada Natural", "Limonada fresca con hielo", 3800, 1600, 3, 5),
            ],
            "🍰 Postres": [
                ("Torta de Chocolate", "Deliciosa torta de chocolate con crema", 8000, 3500, 15, 25),
                ("Helado Artesanal", "3 bolas de helado con topping a elección", 6000, 2800, 5, 15),
                ("Flan de Caramelo", "Flan casero con caramelo natural", 5000, 2200, 20, 30),
                ("Brownie con Helado", "Brownie caliente con helado de vainilla", 7000, 3200, 20, 35),
            ],
            "🌮 Mexicana": [
                ("Tacos al Pastor", "3 tacos con carne al pastor, piña y cilantro", 14000, 6500, 20, 30),
                ("Quesadillas", "Tortilla con queso derretido y pollo", 12000, 5500, 15, 25),
                ("Burrito Supremo", "Burrito grande con carne, frijoles y queso", 16000, 7500, 25, 40),
                ("Nachos Supreme", "Nachos con queso, guacamole y pico de gallo", 13000, 6000, 15, 25),
            ],
            "🍝 Pasta": [
                ("Spaghetti Bolognesa", "Pasta con salsa de carne tradicional", 15000, 7000, 25, 35),
                ("Lasagna Casera", "Lasagna de carne con queso gratinado", 18000, 8500, 40, 60),
                ("Fettuccine Alfredo", "Pasta cremosa con salsa alfredo", 16000, 7500, 20, 30),
                ("Carbonara", "Spaghetti con bacon, huevo y queso", 17000, 8000, 25, 35),
            ],
            "🥪 Sándwiches": [
                ("Club Sandwich", "Triple sandwich con pollo, bacon y vegetales", 14000, 6500, 20, 30),
                ("Sándwich de Jamón", "Pan artesanal con jamón serrano y queso", 10000, 4500, 15, 20),
                ("Wrap de Pollo", "Tortilla con pollo, vegetales y aderezo", 12000, 5500, 15, 25),
                ("Panini Italiano", "Pan prensado con mortadela, salami y queso", 13000, 6000, 18, 28),
            ]
        }
        
        total_products = 0
        for category in categories:
            if category.name in products_by_category:
                products_data = products_by_category[category.name]
                for name, description, price, cost, prep_time, stock in products_data:
                    product = Product(
                        name=name,
                        description=description,
                        price=Decimal(str(price)),
                        cost=Decimal(str(cost)),
                        category_id=category.id,
                        preparation_time=prep_time,
                        stock=stock,
                        is_active=True,
                        is_featured=choice([True, False]) if total_products % 4 == 0 else False
                    )
                    self.db.add(product)
                    total_products += 1
        
        self.db.commit()
        print(f"✅ {total_products} productos creados")
    
    def generate_users(self):
        """Generar usuarios de prueba"""
        users = [
            User(
                username="admin",
                password="admin123",
                full_name="Administrador Principal",
                email="admin@restaurant.com",
                role=UserRole.ADMIN
            ),
            User(
                username="cashier",
                password="cashier123",
                full_name="Cajero Principal",
                email="cashier@restaurant.com",
                role=UserRole.REGULAR
            ),
            User(
                username="cook",
                password="cook123",
                full_name="Chef Principal",
                email="cook@restaurant.com",
                role=UserRole.REGULAR
            )
        ]
        
        # Guardar usuarios en la base de datos
        for user in users:
            self.db.add(user)
        
        self.db.commit()
        print(f"✅ {len(users)} usuarios creados")
    
    def create_historical_orders(self):
        """Crear órdenes históricas para reportes"""
        products = self.db.query(Product).all()
        
        # Generar órdenes de los últimos 90 días
        start_date = datetime.now() - timedelta(days=90)
        total_orders = 0
        
        for days_back in range(90):
            order_date = start_date + timedelta(days=days_back)
            
            # Número variable de órdenes por día (más en fines de semana)
            if order_date.weekday() >= 5:  # Sábado y domingo
                daily_orders = randint(15, 35)
            else:  # Días laborales
                daily_orders = randint(8, 20)
            
            for _ in range(daily_orders):
                # Crear orden
                customer_names = [
                    "Juan Pérez", "María García", "Carlos López", "Ana Martínez",
                    "Luis Rodriguez", "Carmen Sánchez", "Pedro González", "Laura Torres",
                    "Miguel Herrera", "Rosa Jiménez", "Cliente", "Mesa 1", "Mesa 2"
                ]
                
                order = Order(
                    customer_name=choice(customer_names),
                    table_number=randint(1, 15) if choice([True, False]) else None,
                    status=choice([OrderStatus.DELIVERED.value, OrderStatus.PAID.value]),
                    payment_method=choice(["efectivo", "tarjeta", "transferencia"]),
                    created_at=order_date.replace(
                        hour=randint(10, 22),
                        minute=randint(0, 59),
                        second=randint(0, 59)
                    ),
                    total=0  # Se calculará después
                )
                
                self.db.add(order)
                self.db.flush()  # Para obtener el ID
                
                # Añadir items a la orden (1-5 productos por orden)
                order_total = 0
                num_items = randint(1, 5)
                selected_products = []
                
                for _ in range(num_items):
                    product = choice(products)
                    if product not in selected_products:
                        selected_products.append(product)
                        quantity = randint(1, 3)
                        
                        order_item = OrderItem(
                            order_id=order.id,
                            product_id=product.id,
                            quantity=quantity,
                            unit_price=float(product.price),
                            subtotal=float(product.price) * quantity
                        )
                        
                        self.db.add(order_item)
                        order_total += order_item.subtotal
                
                # Actualizar total de la orden
                order.total = order_total
                total_orders += 1
        
        self.db.commit()
        print(f"✅ {total_orders} órdenes históricas creadas")
        
        # Mostrar estadísticas
        self.show_statistics()
    
    def show_statistics(self):
        """Mostrar estadísticas de los datos generados"""
        try:
            categories_count = self.db.query(Category).count()
            products_count = self.db.query(Product).count()
            orders_count = self.db.query(Order).count()
            
            # Calcular ventas totales
            total_sales = self.db.query(func.sum(Order.total)).scalar() or 0
            
            # Ventas del último mes
            last_month = datetime.now() - timedelta(days=30)
            monthly_sales = self.db.query(func.sum(Order.total)).filter(
                Order.created_at >= last_month
            ).scalar() or 0
            
            print("\n" + "="*50)
            print("📊 ESTADÍSTICAS DE DATOS GENERADOS")
            print("="*50)
            print(f"📁 Categorías: {categories_count}")
            print(f"🍽️  Productos: {products_count}")
            print(f"🛒 Órdenes: {orders_count}")
            print(f"💰 Ventas totales: ${total_sales:,.0f} COP")
            print(f"📅 Ventas último mes: ${monthly_sales:,.0f} COP")
            print("="*50)
            print("🎯 La base de datos está lista para probar reportes y gráficas!")
            
        except Exception as e:
            print(f"❌ Error calculando estadísticas: {e}")

def main():
    """Función principal"""
    print("🚀 Generador de Base de Datos de Prueba")
    print("="*50)
    
    # Confirmar con el usuario
    confirm = input("¿Deseas generar una nueva base de datos con datos de prueba? (s/N): ")
    if confirm.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Generar datos
    generator = TestDataGenerator()
    generator.create_test_database()

if __name__ == "__main__":
    main()
