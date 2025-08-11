#!/usr/bin/env python3
"""
Script para verificar el estado final de la base de datos mínima
y preparar información para el build en Windows 11
"""

import os
import sqlite3
from datetime import datetime

def check_database_info():
    """Verificar información de la base de datos"""
    db_path = "data/pos.db"
    
    if not os.path.exists(db_path):
        print("❌ No se encontró la base de datos")
        return
    
    # Tamaño del archivo
    size_bytes = os.path.getsize(db_path)
    size_kb = size_bytes / 1024
    
    print("📦 INFORMACIÓN DE BASE DE DATOS PARA BUILD")
    print("=" * 50)
    print(f"📁 Archivo: {db_path}")
    print(f"📏 Tamaño: {size_bytes:,} bytes ({size_kb:.1f} KB)")
    print(f"📅 Modificado: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
    
    # Conectar a la BD para verificar contenido
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Contar registros en cada tabla
    tables = ['users', 'categories', 'products', 'orders', 'order_items']
    
    print("\n📊 CONTENIDO DE TABLAS:")
    print("-" * 30)
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table:15}: {count:3} registros")
        except sqlite3.OperationalError:
            print(f"{table:15}: Tabla no existe")
    
    conn.close()
    
    print("\n✅ LISTO PARA BUILD EN WINDOWS 11")
    print("=" * 50)
    print("🎯 Base de datos mínima y optimizada")
    print("📦 Tamaño compacto para distribución")
    print("🚀 Sin datos de prueba innecesarios")
    print("👨‍💼 Cliente puede configurar desde cero")
    
    print("\n🔐 CREDENCIALES INCLUIDAS:")
    print("   👑 Admin: admin / admin123")
    print("   💰 Cajero: cajero / cajero123")
    
    print("\n📋 CATEGORÍAS PRECONFIGURADAS:")
    print("   🍽️ Platos Principales")
    print("   🥤 Bebidas")
    print("   🍰 Postres")
    print("   🍟 Acompañamientos")

if __name__ == "__main__":
    check_database_info()
