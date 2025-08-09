#!/usr/bin/env python3
"""
Script para generar datos de prueba para el sistema POS
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.base import get_db
from models.user import User
from models.category import Category
from models.product import Product
from models.order import Order
from models.order_item import OrderItem

def create_test_data():
    """Crear datos de prueba para el sistema"""
    print("🏗️ Generando datos de prueba...")
    
    # Inicializar base de datos
    session = get_db()
    
    try:
        # Verificar si ya existen productos
        existing_products = session.query(Product).count()
        if existing_products > 0:
            print(f"⚠️ Ya existen {existing_products} productos. ¿Continuar? (y/N)")
            response = input().lower()
            if response != 'y':
                print("❌ Operación cancelada")
                return
        
        # 1. Crear categorías si no existen
        categories_data = [
            {"name": "Hamburguesas", "description": "Deliciosas hamburguesas gourmet"},
            {"name": "Bebidas", "description": "Refrescos, jugos y bebidas calientes"},
            {"name": "Acompañamientos", "description": "Papas fritas, aros de cebolla, ensaladas"},
            {"name": "Postres", "description": "Dulces tentaciones para terminar la comida"}
        ]
        
        categories = {}
        for cat_data in categories_data:
            existing_cat = session.query(Category).filter_by(name=cat_data["name"]).first()
            if not existing_cat:
                category = Category(
                    name=cat_data["name"],
                    description=cat_data["description"]
                )
                session.add(category)
                session.flush()
                categories[cat_data["name"]] = category
                print(f"✅ Categoría creada: {cat_data['name']}")
            else:
                categories[cat_data["name"]] = existing_cat
                print(f"📁 Categoría existente: {cat_data['name']}")
        
        # 2. Crear productos
        products_data = [
            # Hamburguesas
            {"name": "Hamburguesa Clásica", "price": 12.99, "category": "Hamburguesas"},
            {"name": "Hamburguesa BBQ", "price": 14.99, "category": "Hamburguesas"},
            {"name": "Hamburguesa Vegetariana", "price": 11.99, "category": "Hamburguesas"},
            {"name": "Hamburguesa Doble Carne", "price": 16.99, "category": "Hamburguesas"},
            
            # Bebidas
            {"name": "Coca Cola", "price": 2.99, "category": "Bebidas"},
            {"name": "Agua Natural", "price": 1.99, "category": "Bebidas"},
            {"name": "Jugo de Naranja", "price": 3.49, "category": "Bebidas"},
            {"name": "Café Americano", "price": 2.49, "category": "Bebidas"},
            
            # Acompañamientos
            {"name": "Papas Fritas", "price": 4.99, "category": "Acompañamientos"},
            {"name": "Aros de Cebolla", "price": 5.99, "category": "Acompañamientos"},
            {"name": "Ensalada César", "price": 7.99, "category": "Acompañamientos"},
            
            # Postres
            {"name": "Helado de Vainilla", "price": 4.49, "category": "Postres"},
            {"name": "Pastel de Chocolate", "price": 6.99, "category": "Postres"},
        ]
        
        products = {}
        for prod_data in products_data:
            existing_prod = session.query(Product).filter_by(name=prod_data["name"]).first()
            if not existing_prod:
                product = Product(
                    name=prod_data["name"],
                    price=prod_data["price"],
                    category_id=categories[prod_data["category"]].id,
                    is_active=True
                )
                session.add(product)
                session.flush()
                products[prod_data["name"]] = product
                print(f"🍽️ Producto creado: {prod_data['name']} - ${prod_data['price']}")
            else:
                products[prod_data["name"]] = existing_prod
        
        # 3. Crear órdenes de prueba para los últimos 30 días
        print("📋 Generando órdenes de prueba...")
        
        # Obtener todos los productos
        all_products = list(products.values())
        if not all_products:
            all_products = session.query(Product).all()
        
        # Generar órdenes para los últimos 30 días
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        total_orders = 0
        for day_offset in range(30):
            current_date = start_date + timedelta(days=day_offset)
            
            # Variar la cantidad de órdenes por día (más en fines de semana)
            if current_date.weekday() >= 5:  # Sábado y domingo
                daily_orders = random.randint(15, 25)
            else:
                daily_orders = random.randint(8, 15)
            
            for order_num in range(daily_orders):
                # Crear orden con total inicial
                order = Order(
                    customer_name=f"Cliente {random.randint(1, 100)}",
                    table_number=random.choice([None, f"Mesa {random.randint(1, 10)}"]),
                    status=random.choice(['completed', 'paid']),
                    total=0.0,  # Inicializar con 0, se actualizará después
                    created_at=current_date + timedelta(
                        hours=random.randint(10, 21),
                        minutes=random.randint(0, 59)
                    )
                )
                session.add(order)
                session.flush()
                
                # Agregar items a la orden (1-4 productos por orden)
                num_items = random.randint(1, 4)
                order_total = 0
                
                selected_products = random.sample(all_products, min(num_items, len(all_products)))
                
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    unit_price = float(product.price)
                    subtotal = quantity * unit_price
                    
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )
                    session.add(order_item)
                    order_total += subtotal
                
                # Actualizar total de la orden
                order.total = order_total
                total_orders += 1
        
        # Commit todos los cambios
        session.commit()
        print(f"✅ {total_orders} órdenes de prueba creadas exitosamente!")
        print(f"📊 Datos generados para el período: {start_date.date()} a {end_date.date()}")
        
        # Mostrar estadísticas
        total_sales = sum([order.total for order in session.query(Order).filter(Order.status.in_(['completed', 'paid'])).all()])
        print(f"💰 Ingresos totales generados: ${total_sales:.2f}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error generando datos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    create_test_data()
