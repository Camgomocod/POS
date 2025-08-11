#!/usr/bin/env python3
"""
Script para generar una base de datos mínima para build/distribución
Solo incluye usuarios esenciales y categorías básicas
"""

import os
import sys
import shutil
from datetime import datetime

# Añadir el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import Base, engine, create_tables, get_db
from models.category import Category
from models.user import User, UserRole

class MinimalDataGenerator:
    """Generador de datos mínimos para distribución"""
    
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
    
    def create_minimal_database(self):
        """Crear base de datos mínima para distribución"""
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
            
            # Generar datos mínimos
            self.create_essential_users()
            self.create_basic_categories()
            
            print("🎉 Base de datos mínima generada exitosamente!")
            print("📦 Lista para build/distribución en Windows 11")
            
        except Exception as e:
            print(f"❌ Error generando base de datos: {e}")
            self.db.rollback()
    
    def create_essential_users(self):
        """Crear usuarios esenciales para el sistema"""
        users = [
            User(
                username="admin",
                password="admin123",
                full_name="Administrador del Sistema",
                email="admin@mirestaurante.com",
                role=UserRole.ADMIN
            ),
            User(
                username="cajero",
                password="cajero123",
                full_name="Cajero Principal",
                email="cajero@mirestaurante.com",
                role=UserRole.REGULAR
            )
        ]
        
        # Guardar usuarios en la base de datos
        for user in users:
            self.db.add(user)
        
        self.db.commit()
        print(f"✅ {len(users)} usuarios esenciales creados")
        
        # Mostrar credenciales
        print("\n👥 CREDENCIALES DE ACCESO:")
        print("=" * 40)
        print("🔐 Administrador:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print()
        print("🔐 Cajero:")
        print("   Usuario: cajero") 
        print("   Contraseña: cajero123")
        print("=" * 40)
    
    def create_basic_categories(self):
        """Crear categorías básicas para empezar"""
        categories_data = [
            ("🍽️ Platos Principales", "Comidas principales del menú"),
            ("🥤 Bebidas", "Refrescos, jugos y bebidas"),
            ("🍰 Postres", "Dulces y postres"),
            ("🍟 Acompañamientos", "Guarniciones y extras")
        ]
        
        for name, description in categories_data:
            category = Category(name=name, description=description, is_active=True)
            self.db.add(category)
        
        self.db.commit()
        print(f"✅ {len(categories_data)} categorías básicas creadas")
    
    def show_minimal_statistics(self):
        """Mostrar estadísticas de la base de datos mínima"""
        try:
            categories_count = self.db.query(Category).count()
            users_count = self.db.query(User).count()
            
            print("\n" + "="*50)
            print("📊 ESTADÍSTICAS DE BASE DE DATOS MÍNIMA")
            print("="*50)
            print(f"👥 Usuarios: {users_count}")
            print(f"📁 Categorías: {categories_count}")
            print(f"🍽️ Productos: 0 (listo para agregar)")
            print(f"🛒 Órdenes: 0 (listo para usar)")
            print("="*50)
            print("🎯 Base de datos lista para distribución!")
            print("📦 Preparada para build en Windows 11")
            print("🚀 El administrador puede comenzar a configurar el menú")
            
        except Exception as e:
            print(f"❌ Error calculando estadísticas: {e}")

def main():
    """Función principal"""
    print("🏗️  Generador de Base de Datos Mínima para Build")
    print("="*60)
    print("📦 Esta versión incluye solo lo esencial:")
    print("   - 2 usuarios (admin y cajero)")
    print("   - 4 categorías básicas")
    print("   - Sin productos (para que el cliente configure)")
    print("   - Sin órdenes históricas")
    print()
    
    # Confirmar con el usuario
    confirm = input("¿Deseas generar la base de datos mínima para build? (s/N): ")
    if confirm.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Generar datos mínimos
    generator = MinimalDataGenerator()
    generator.create_minimal_database()
    generator.show_minimal_statistics()
    
    print("\n✨ PRÓXIMOS PASOS PARA BUILD:")
    print("1. 🔧 Verificar que la aplicación funciona correctamente")
    print("2. 📦 Ejecutar el script de build para Windows 11")
    print("3. 🚀 Distribuir la aplicación con esta base de datos limpia")
    print("4. 👨‍💼 El cliente puede configurar productos según su negocio")

if __name__ == "__main__":
    main()
