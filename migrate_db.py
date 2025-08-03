#!/usr/bin/env python3
"""
Script de migración para agregar el campo payment_method y el estado PAID
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import get_db, engine
from models.order import Order, OrderStatus
from sqlalchemy import text
import sqlalchemy

def migrate_database():
    """Ejecutar migración de base de datos"""
    db = get_db()
    
    try:
        # Verificar si la columna payment_method ya existe
        inspector = sqlalchemy.inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('orders')]
        
        if 'payment_method' not in columns:
            print("Agregando columna payment_method...")
            # Agregar columna payment_method
            db.execute(text("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50)"))
            db.commit()
            print("✅ Columna payment_method agregada")
        else:
            print("ℹ️  Columna payment_method ya existe")
        
        # Verificar si el estado PAID existe en los datos
        print("Verificando estado PAID...")
        
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
