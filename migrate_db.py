#!/usr/bin/env python3
"""
Script de migración para actualizar la base de datos con nuevas funcionalidades
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import get_db, engine, create_tables
from models.order import Order, OrderStatus
from models.user import User, UserRole
from sqlalchemy import text
import sqlalchemy

def migrate_database():
    """Ejecutar migración de base de datos"""
    db = get_db()
    
    try:
        print("🔄 Iniciando migración de base de datos...")
        
        # Crear todas las tablas (incluye la nueva tabla users)
        create_tables()
        print("✅ Tablas creadas/actualizadas")
        
        # Verificar si la columna payment_method ya existe en orders
        inspector = sqlalchemy.inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('orders')]
        
        if 'payment_method' not in columns:
            print("📝 Agregando columna payment_method...")
            # Agregar columna payment_method
            db.execute(text("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50)"))
            db.commit()
            print("✅ Columna payment_method agregada")
        else:
            print("ℹ️  Columna payment_method ya existe")
        
        # Verificar si ya existen usuarios en la base de datos
        user_count = db.query(User).count()
        if user_count == 0:
            print("👥 Creando usuarios por defecto...")
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
            print(f"✅ Creados {len(default_users)} usuarios por defecto")
        else:
            print(f"ℹ️  Ya existen {user_count} usuarios en la base de datos")
        
        # Actualizar órdenes existentes que no tengan método de pago
        result = db.execute(text("UPDATE orders SET payment_method = 'efectivo' WHERE payment_method IS NULL"))
        if result.rowcount > 0:
            print(f"✅ Actualizado payment_method en {result.rowcount} órdenes")
        
        db.commit()
        print("🎉 Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando migración de base de datos...")
    migrate_database()
