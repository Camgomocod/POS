# controllers/app_controller.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal
from views.login_window import LoginWindow
from views.pos_window import POSWindow
from views.admin_window import AdminWindow
from models.user import UserRole

class AppController(QObject):
    """Controlador principal de la aplicación que maneja el flujo entre ventanas"""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.login_window = None
        self.pos_window = None
        self.admin_window = None
        
    def start_application(self):
        """Iniciar la aplicación mostrando el login"""
        try:
            self.show_login()
        except Exception as e:
            print(f"❌ Error al iniciar aplicación: {e}")
            import traceback
            traceback.print_exc()
    
    def show_login(self):
        """Mostrar ventana de login"""
        try:
            # Cerrar ventanas existentes de forma segura
            self.close_all_windows()
            
            # Crear y mostrar login
            self.login_window = LoginWindow()
            self.login_window.login_successful.connect(self.handle_successful_login)
            self.login_window.show()
            
        except Exception as e:
            print(f"❌ Error al mostrar login: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_successful_login(self, user):
        """Manejar login exitoso"""
        try:
            print(f"✅ Login exitoso para usuario: {user.username} (Rol: {user.role.value})")
            self.current_user = user
            
            # Cerrar ventana de login de forma segura
            if self.login_window:
                self.login_window.close()
                self.login_window.deleteLater()  # Asegurar limpieza de memoria
                self.login_window = None
            
            # Mostrar ventana correspondiente según el rol
            if user.role == UserRole.ADMIN:
                self.show_admin_window()
            else:
                self.show_pos_window()
                
        except Exception as e:
            print(f"❌ Error al manejar login exitoso: {e}")
            import traceback
            traceback.print_exc()
    
    def show_pos_window(self):
        """Mostrar ventana POS para usuarios regulares"""
        try:
            print("🍽️ Iniciando ventana POS...")
            self.pos_window = POSWindow()
            
            # Conectar señal de logout
            self.pos_window.logout_requested.connect(self.handle_logout)
            
            self.pos_window.show()
            print("✅ Ventana POS mostrada")
            
        except Exception as e:
            print(f"❌ Error al mostrar ventana POS: {e}")
            import traceback
            traceback.print_exc()
    
    def show_admin_window(self):
        """Mostrar ventana de administración para administradores"""
        try:
            print("⚙️ Iniciando ventana de administración...")
            self.admin_window = AdminWindow(self.current_user)
            self.admin_window.logout_requested.connect(self.handle_logout)
            self.admin_window.show()
            print("✅ Ventana de administración mostrada")
            
        except Exception as e:
            print(f"❌ Error al mostrar ventana admin: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_logout(self):
        """Manejar cierre de sesión"""
        try:
            print("🚪 Procesando logout...")
            self.current_user = None
            self.close_all_windows()
            self.show_login()
            
        except Exception as e:
            print(f"❌ Error en logout: {e}")
            import traceback
            traceback.print_exc()
    
    def close_all_windows(self):
        """Cerrar todas las ventanas abiertas de forma segura"""
        try:
            windows = [
                ('login', self.login_window),
                ('pos', self.pos_window), 
                ('admin', self.admin_window)
            ]
            
            for name, window in windows:
                if window:
                    print(f"🔒 Cerrando ventana {name}...")
                    try:
                        window.close()
                        window.deleteLater()  # Asegurar limpieza de memoria
                    except Exception as e:
                        print(f"⚠️  Error al cerrar ventana {name}: {e}")
            
            # Limpiar referencias
            self.login_window = None
            self.pos_window = None
            self.admin_window = None
            
        except Exception as e:
            print(f"❌ Error al cerrar ventanas: {e}")
            import traceback
            traceback.print_exc()
    
    def quit_application(self):
        """Cerrar completamente la aplicación"""
        self.close_all_windows()
        QApplication.quit()
