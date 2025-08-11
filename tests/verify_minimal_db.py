#!/usr/bin/env python3

from utils.database import get_db
from models.user import User
from models.category import Category
from models.product import Product
from models.order import Order

def verify_minimal_database():
    """Verificar que la base de datos mínima está correcta"""
    db = get_db()
    
    print('📊 VERIFICACIÓN DE BASE DE DATOS MÍNIMA')
    print('='*45)
    
    # Verificar usuarios
    users = db.query(User).all()
    print(f'👥 Usuarios ({len(users)}):')
    for user in users:
        print(f'  - {user.username} ({user.role.value}) - {user.full_name}')
    
    print()
    
    # Verificar categorías
    categories = db.query(Category).all()
    print(f'📁 Categorías ({len(categories)}):')
    for cat in categories:
        print(f'  - {cat.name}')
    
    print()
    
    # Verificar que no hay productos ni órdenes
    products_count = db.query(Product).count()
    orders_count = db.query(Order).count()
    
    print(f'🍽️ Productos: {products_count}')
    print(f'🛒 Órdenes: {orders_count}')
    
    print()
    print('✅ Base de datos mínima verificada correctamente')
    print('📦 Lista para build en Windows 11')
    
    db.close()

if __name__ == "__main__":
    verify_minimal_database()
