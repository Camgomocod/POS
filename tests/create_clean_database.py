#!/usr/bin/env python3
"""
Script para crear una base de datos limpia y mínima para testing y build
Solo incluye usuarios básicos y estructura esencial
"""
import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.base import get_db, engine, Base
from models.user import User, UserRole
from models.category import Category
from models.product import Product

def delete_existing_database():
    """Eliminar base de datos existente si existe"""
    db_files = [
        "data/pos.db",
        "data/pos.db-shm", 
        "data/pos.db-wal",
        "data/pos_backup.db"
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"🗑️ Eliminado: {db_file}")
            except Exception as e:
                print(f"⚠️ Error al eliminar {db_file}: {e}")

def create_fresh_database():
    """Crear estructura de base de datos limpia"""
    print("🏗️ Creando estructura de base de datos limpia...")
    
    # Asegurar que el directorio data existe
    os.makedirs("data", exist_ok=True)
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Estructura de base de datos creada")

def create_basic_users():
    """Crear solo usuarios básicos para testing"""
    print("👥 Creando usuarios básicos...")
    db = get_db()
    
    try:
        # Usuarios básicos para testing
        basic_users = [
            {
                "username": "admin",
                "password": "admin123",
                "full_name": "Administrador",
                "email": "admin@pos.local",
                "role": UserRole.ADMIN
            },
            {
                "username": "cajero",
                "password": "cajero123",
                "full_name": "Cajero",
                "email": "cajero@pos.local",
                "role": UserRole.REGULAR
            }
        ]
        
        for user_data in basic_users:
            user = User(
                username=user_data["username"],
                password=user_data["password"],
                full_name=user_data["full_name"],
                email=user_data["email"],
                role=user_data["role"]
            )
            db.add(user)
            print(f"  ✅ Usuario creado: {user_data['username']} ({user_data['role'].value})")
        
        db.commit()
        print(f"✅ {len(basic_users)} usuarios básicos creados")
        
    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_minimal_categories():
    """Crear categorías mínimas necesarias"""
    print("📂 Creando categorías básicas...")
    db = get_db()
    
    try:
        # Categorías básicas
        basic_categories = [
            {"name": "General", "description": "Productos generales"},
            {"name": "Bebidas", "description": "Bebidas y refrescos"},
        ]
        
        for cat_data in basic_categories:
            category = Category(**cat_data)
            db.add(category)
            print(f"  ✅ Categoría creada: {cat_data['name']}")
        
        db.commit()
        print(f"✅ {len(basic_categories)} categorías básicas creadas")
        
    except Exception as e:
        print(f"❌ Error creando categorías: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def verify_database():
    """Verificar que la base de datos fue creada correctamente"""
    print("🔍 Verificando base de datos...")
    db = get_db()
    
    try:
        # Verificar usuarios
        users = db.query(User).all()
        print(f"  👥 Usuarios en BD: {len(users)}")
        for user in users:
            print(f"    - {user.username} ({user.role.value}) - {user.full_name}")
        
        # Verificar categorías
        categories = db.query(Category).all()
        print(f"  📂 Categorías en BD: {len(categories)}")
        for category in categories:
            print(f"    - {category.name}")
        
        # Verificar productos
        products = db.query(Product).all()
        print(f"  🍔 Productos en BD: {len(products)}")
        
        # Tamaño de la base de datos
        db_path = "data/pos.db"
        if os.path.exists(db_path):
            size_mb = os.path.getsize(db_path) / 1024 / 1024
            print(f"  💾 Tamaño de BD: {size_mb:.2f} MB")
        
        print("✅ Base de datos verificada correctamente")
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        raise
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 Iniciando creación de base de datos limpia para testing...")
    print("=" * 60)
    
    try:
        # Paso 1: Eliminar base de datos existente
        delete_existing_database()
        print()
        
        # Paso 2: Crear estructura limpia
        create_fresh_database()
        print()
        
        # Paso 3: Crear usuarios básicos
        create_basic_users()
        print()
        
        # Paso 4: Crear categorías mínimas
        create_minimal_categories()
        print()
        
        # Paso 5: Verificar
        verify_database()
        print()
        
        print("=" * 60)
        print("🎉 ¡Base de datos limpia creada exitosamente!")
        print()
        print("📝 Credenciales de acceso:")
        print("   👤 Administrador:")
        print("      Usuario: admin")
        print("      Contraseña: admin123")
        print()
        print("   👤 Cajero:")
        print("      Usuario: cajero") 
        print("      Contraseña: cajero123")
        print()
        print("🚀 El sistema está listo para testing y build")
        
    except Exception as e:
        print(f"\n❌ Error durante la creación: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
