#!/usr/bin/env python3
# test_user_management.py - Script para probar la gestión de usuarios

import sys
sys.path.append('.')

from PyQt5.QtWidgets import QApplication, QMainWindow
from views.user_management_window import UserManagementWidget
from models.user import User, UserRole
from controllers.auth_controller import AuthController
from utils.database import DatabaseManager

def test_user_management():
    """Probar la gestión de usuarios"""
    app = QApplication(sys.argv)
    
    # Crear usuario admin de prueba
    auth_ctrl = AuthController()
    
    # Intentar obtener un usuario admin existente
    users = auth_ctrl.get_all_users()
    admin_user = None
    
    for user in users:
        if user.role == UserRole.ADMIN and user.is_active:
            admin_user = user
            break
    
    if not admin_user:
        print("No se encontró usuario administrador. Creando uno...")
        success, admin_user, message = auth_ctrl.create_user(
            username="admin",
            password="admin123",
            full_name="Administrador del Sistema",
            email="admin@pos.com",
            role=UserRole.ADMIN
        )
        
        if not success:
            print(f"Error creando admin: {message}")
            return
        print(f"Admin creado: {message}")
    
    # Crear ventana principal
    window = QMainWindow()
    window.setWindowTitle("🧪 Prueba - Gestión de Usuarios")
    window.resize(1200, 800)
    
    # Crear widget de gestión de usuarios
    user_management = UserManagementWidget(admin_user)
    window.setCentralWidget(user_management)
    
    # Mostrar ventana
    window.show()
    
    print("🚀 Interfaz de gestión de usuarios cargada exitosamente!")
    print("📋 Funcionalidades disponibles:")
    print("   • ➕ Crear nuevos usuarios")
    print("   • ✏️ Editar usuarios existentes") 
    print("   • 🔑 Resetear contraseñas")
    print("   • 🔄 Activar/Desactivar usuarios")
    print("   • 👥 Ver estadísticas de usuarios")
    print("   • 🛡️ Asignar roles (Admin/Regular)")
    print("   • ✅ Validación de duplicados")
    print("   • 🎲 Generador de contraseñas")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_user_management()
