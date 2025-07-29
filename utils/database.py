# utils/database.py
from models.base import create_tables, get_db
from models.category import Category
from models.product import Product

def init_database():
    """Inicializar base de datos con datos de ejemplo"""
    create_tables()
    
    db = get_db()
    
    # Verificar si ya hay datos
    if db.query(Category).count() > 0:
        db.close()
        return
    
    # Categorías de ejemplo
    categories = [
        Category(name="Hamburguesas", description="Hamburguesas variadas"),
        Category(name="Bebidas", description="Bebidas frías y calientes"),
        Category(name="Acompañamientos", description="Papas, ensaladas, etc."),
        Category(name="Postres", description="Postres y dulces")
    ]
    
    for category in categories:
        db.add(category)
    db.commit()
    
    # Productos de ejemplo
    products = [
        # Hamburguesas
        Product(name="Hamburguesa Clásica", price=8.99, category_id=1),
        Product(name="Hamburguesa con Queso", price=9.99, category_id=1),
        Product(name="Hamburguesa Especial", price=12.99, category_id=1),
        
        # Bebidas
        Product(name="Coca Cola", price=2.50, category_id=2),
        Product(name="Agua", price=1.50, category_id=2),
        Product(name="Jugo Natural", price=3.00, category_id=2),
        
        # Acompañamientos
        Product(name="Papas Fritas", price=3.99, category_id=3),
        Product(name="Aros de Cebolla", price=4.50, category_id=3),
        Product(name="Ensalada", price=5.99, category_id=3),
        
        # Postres
        Product(name="Helado", price=3.50, category_id=4),
        Product(name="Torta de Chocolate", price=4.99, category_id=4)
    ]
    
    for product in products:
        db.add(product)
    db.commit()
    db.close()
    
    print("Base de datos inicializada con datos de ejemplo")
