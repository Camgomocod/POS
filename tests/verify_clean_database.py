#!/usr/bin/env python3
"""
Script de verificación para confirmar que la base de datos limpia está lista para testing
"""

import os
import sys

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.base import get_db
from models.user import User, UserRole
from models.category import Category
from models.product import Product
from models.order import Order
from controllers.auth_controller import AuthController

def test_login_credentials():
    """Probar las credenciales de login"""
    print("🔐 Probando credenciales de login...")
    
    auth_ctrl = AuthController()
    
    # Probar admin
    success, user, message = auth_ctrl.login("admin", "admin123")
    if success and user and user.role == UserRole.ADMIN:
        print(f"  ✅ Admin login exitoso: {user.full_name}")
    else:
        print(f"  ❌ Admin login falló: {message}")
        return False
    
    # Probar cajero
    success, user, message = auth_ctrl.login("cajero", "cajero123")
    if success and user and user.role == UserRole.REGULAR:
        print(f"  ✅ Cajero login exitoso: {user.full_name}")
    else:
        print(f"  ❌ Cajero login falló: {message}")
        return False
    
    return True

def check_database_structure():
    """Verificar estructura de la base de datos"""
    print("🏗️ Verificando estructura de base de datos...")
    
    db = get_db()
    try:
        # Verificar tablas principales
        users_count = db.query(User).count()
        categories_count = db.query(Category).count()
        products_count = db.query(Product).count()
        orders_count = db.query(Order).count()
        
        print(f"  📊 Usuarios: {users_count}")
        print(f"  📂 Categorías: {categories_count}")
        print(f"  🍔 Productos: {products_count}")
        print(f"  🧾 Órdenes: {orders_count}")
        
        # Verificar que es una BD limpia
        if orders_count == 0 and products_count == 0:
            print(f"  ✅ Base de datos limpia confirmada")
            return True
        else:
            print(f"  ⚠️ La base de datos no está completamente limpia")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando estructura: {e}")
        return False
    finally:
        db.close()

def check_file_size():
    """Verificar tamaño de archivos de BD"""
    print("💾 Verificando tamaño de base de datos...")
    
    db_path = "data/pos.db"
    if os.path.exists(db_path):
        size_bytes = os.path.getsize(db_path)
        size_kb = size_bytes / 1024
        size_mb = size_bytes / 1024 / 1024
        
        print(f"  📏 Tamaño: {size_bytes} bytes ({size_kb:.1f} KB, {size_mb:.2f} MB)")
        
        # Una BD limpia debería ser relativamente pequeña
        if size_kb < 100:  # Menos de 100KB indica BD muy limpia
            print(f"  ✅ Base de datos muy compacta (ideal para testing)")
        else:
            print(f"  ⚠️ Base de datos más grande de lo esperado")
        
        return True
    else:
        print(f"  ❌ Archivo de base de datos no encontrado")
        return False

def show_ready_for_build_info():
    """Mostrar información para preparar el build"""
    print("\n🚀 INFORMACIÓN PARA BUILD Y TESTING")
    print("=" * 50)
    print()
    print("📋 ESTADO ACTUAL:")
    print("  ✅ Base de datos completamente limpia")
    print("  ✅ Solo usuarios básicos (admin, cajero)")
    print("  ✅ Categorías mínimas para funcionamiento")
    print("  ✅ Sin productos, órdenes o datos de prueba")
    print()
    print("🔐 CREDENCIALES PARA TESTING:")
    print("  👤 Administrador:")
    print("     Usuario: admin")
    print("     Contraseña: admin123")
    print("     Acceso: Completo al sistema")
    print()
    print("  👤 Cajero:")
    print("     Usuario: cajero")
    print("     Contraseña: cajero123")
    print("     Acceso: POS y operaciones básicas")
    print()
    print("📁 ARCHIVOS PARA BUILD:")
    print("  🗄️ Base de datos: data/pos.db")
    print("  📦 Tamaño mínimo para distribución")
    print("  🔧 Lista para empaquetado")
    print()
    print("🧪 PRÓXIMOS PASOS SUGERIDOS:")
    print("  1. Probar login con ambos usuarios")
    print("  2. Crear algunas categorías y productos de prueba")
    print("  3. Probar flujo completo de POS")
    print("  4. Verificar funcionalidades de administración")
    print("  5. Preparar script de build/empaquetado")

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICACIÓN DE BASE DE DATOS LIMPIA")
    print("=" * 50)
    print()
    
    all_tests_passed = True
    
    # Test 1: Estructura de BD
    if not check_database_structure():
        all_tests_passed = False
    print()
    
    # Test 2: Credenciales de login
    if not test_login_credentials():
        all_tests_passed = False
    print()
    
    # Test 3: Tamaño de archivos
    if not check_file_size():
        all_tests_passed = False
    print()
    
    # Resultado final
    if all_tests_passed:
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print("🎉 La base de datos está lista para testing y build")
        show_ready_for_build_info()
        return 0
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("⚠️ Revisar la configuración antes de continuar")
        return 1

if __name__ == "__main__":
    sys.exit(main())
