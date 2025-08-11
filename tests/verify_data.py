#!/usr/bin/env python3

from utils.database import get_db
from models.order import Order
from models.product import Product
from models.category import Category  
from models.user import User
from sqlalchemy import func

def main():
    db = get_db()
    print('📊 Resumen de datos generados:')
    print(f'- Categorías: {db.query(Category).count()}')
    print(f'- Productos: {db.query(Product).count()}')  
    print(f'- Usuarios: {db.query(User).count()}')
    print(f'- Órdenes: {db.query(Order).count()}')
    
    total_sales = db.query(func.sum(Order.total)).scalar() or 0
    print(f'- Ventas totales: ${total_sales:,.0f} COP')
    
    # Verificar algunas categorías
    print('\n📂 Categorías disponibles:')
    categories = db.query(Category).limit(5).all()
    for cat in categories:
        product_count = db.query(Product).filter(Product.category_id == cat.id).count()
        print(f'  - {cat.name}: {product_count} productos')
    
    db.close()

if __name__ == "__main__":
    main()
