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
        self.show_login()
    
    def show_login(self):
        """Mostrar ventana de login"""
        # Cerrar ventanas existentes
        self.close_all_windows()
        
        # Crear y mostrar login
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.handle_successful_login)
        self.login_window.show()
    
    def handle_successful_login(self, user):
        """Manejar login exitoso"""
        self.current_user = user
        
        # Cerrar ventana de login
        if self.login_window:
            self.login_window.close()
            self.login_window = None
        
        # Mostrar ventana correspondiente según el rol
        if user.role == UserRole.ADMIN:
            self.show_admin_window()
        else:
            self.show_pos_window()
    
    def show_pos_window(self):
        """Mostrar ventana POS para usuarios regulares"""
        self.pos_window = POSWindow()
        
        # Conectar señal de logout
        self.pos_window.logout_requested.connect(self.handle_logout)
        
        self.pos_window.show()
    
    def show_admin_window(self):
        """Mostrar ventana de administración para administradores"""
        self.admin_window = AdminWindow(self.current_user)
        self.admin_window.logout_requested.connect(self.handle_logout)
        self.admin_window.show()
    
    def handle_logout(self):
        """Manejar cierre de sesión"""
        self.current_user = None
        self.close_all_windows()
        self.show_login()
    
    def close_all_windows(self):
        """Cerrar todas las ventanas abiertas"""
        windows = [self.login_window, self.pos_window, self.admin_window]
        
        for window in windows:
            if window:
                window.close()
        
        # Limpiar referencias
        self.login_window = None
        self.pos_window = None
        self.admin_window = None
    
    def quit_application(self):
        """Cerrar completamente la aplicación"""
        self.close_all_windows()
        QApplication.quit()
