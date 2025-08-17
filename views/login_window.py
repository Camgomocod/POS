# views/login_window.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QFrame, QApplication, QMessageBox,
                             QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from controllers.auth_controller import AuthController
from models.user import UserRole
from utils.colors import ColorPalette
import sys

class LoginWindow(QMainWindow):
    """Ventana de inicio de sesión simple"""
    
    # Señales para comunicación
    login_successful = pyqtSignal(object)  # Emite el objeto usuario
    
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.init_ui()
        
    def init_ui(self):
        """Configurar interfaz de usuario simplificada"""
        # Configuración de ventana - tamaño compacto
        self.setWindowTitle("Iniciar Sesión")
        self.setFixedSize(440, 420)  # Ventana compacta
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Centrar ventana
        self.center_window()
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal compacto
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Márgenes reducidos
        main_layout.setSpacing(12)  # Espaciado reducido
        
        # Título principal compacto
        title_label = QLabel("Asados al Karbon")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #415a77;
                margin-bottom: 5px;
                padding: 5px;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Formulario compacto
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)  # Espaciado reducido
        
        # Campo usuario compacto
        user_label = QLabel("👤 Usuario")
        user_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #0d1b2a;
                margin-bottom: 5px;
            }
        """)
        form_layout.addWidget(user_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu nombre de usuario")
        self.username_input.setText("admin")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 5px 5px;
                border: 2px solid #778da9;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                min-height: 20px;
                selection-background-color: #415a77;
            }
            QLineEdit:focus {
                border-color: #415a77;
                background-color: #f8f9fa;
            }
            QLineEdit:hover {
                border-color: #415a77;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # Campo contraseña compacto
        password_label = QLabel("🔒 Contraseña")
        password_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #0d1b2a;
                margin-bottom: 5px;
            }
        """)
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText("admin123")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 5px 5px;
                border: 2px solid #778da9;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                min-height: 20px;
                selection-background-color: #415a77;
            }
            QLineEdit:focus {
                border-color: #415a77;
                background-color: #f8f9fa;
            }
            QLineEdit:hover {
                border-color: #415a77;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        main_layout.addLayout(form_layout)
        
        # Botones compactos
        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(0, 20, 0, 20)  # Espaciado reducido

        # Botón iniciar sesión compacto
        self.login_btn = QPushButton("🚀 Iniciar Sesión")
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #415a77, stop:1 #1b263b);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #778da9, stop:1 #415a77);
            }
            QPushButton:pressed {
                background-color: #0d1b2a;
            }
            QPushButton:disabled {
                background-color: #778da9;
                color: #e0e1dd;
            }
        """)
        buttons_layout.addWidget(self.login_btn)
        
        # Botón salir compacto
        self.exit_btn = QPushButton("❌ Salir")
        self.exit_btn.clicked.connect(self.close_application)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e1dd;
                color: #0d1b2a;
                border: 2px solid #778da9;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #778da9;
                color: white;
                border-color: #415a77;
            }
            QPushButton:pressed {
                background-color: #415a77;
            }
        """)
        buttons_layout.addWidget(self.exit_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Conectar Enter para login
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.handle_login)
        
        # Estilo general con gradiente sutil
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #f8f9fa, stop:0.5 #e9ecef, stop:1 #dee2e6);
            }
        """)
    
    def center_window(self):
        """Centrar ventana en la pantalla"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def handle_login(self):
        """Manejar intento de login"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_message("Error", "Por favor ingresa usuario y contraseña", "warning")
            return
        
        # Deshabilitar botón durante el proceso
        self.login_btn.setEnabled(False)
        self.login_btn.setText("🔄 Verificando...")
        
        # Procesar login directamente
        self.process_login(username, password)
    
    def process_login(self, username, password):
        """Procesar login con el controlador"""
        success, user, message = self.auth_controller.login(username, password)
        
        if success:
            # No mostrar mensaje, solo emitir señal directamente
            self.login_successful.emit(user)
        else:
            self.show_message("❌ Error de Autenticación", message, "error")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("🚀 Iniciar Sesión")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def show_message(self, title, message, msg_type="info"):
        """Mostrar mensaje estilizado"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # Estilo según tipo de mensaje
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Information)
            icon_style = f"background-color: {ColorPalette.SUCCESS};"
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
            icon_style = f"background-color: {ColorPalette.ERROR};"
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
            icon_style = f"background-color: {ColorPalette.WARNING};"
        else:
            msg_box.setIcon(QMessageBox.Information)
            icon_style = f"background-color: {ColorPalette.YINMN_BLUE};"
        
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
                font-size: 13px;
            }}
            QMessageBox QLabel {{
                color: {ColorPalette.RICH_BLACK};
                padding: 10px;
            }}
            QMessageBox QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        
        msg_box.exec_()
    
    def close_application(self):
        """Cerrar aplicación completamente"""
        reply = QMessageBox.question(self, "Confirmar Salida", 
                                   "¿Estás seguro de que deseas salir?",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
    
    def closeEvent(self, event):
        """Manejar cierre de ventana"""
        # Solo pedir confirmación si el cierre es iniciado por el usuario
        if event.spontaneous():
            # Cuando el usuario cierra la ventana manualmente, confirmar salida
            self.close_application()
            event.ignore()  # Ignorar el cierre si el usuario no confirma
        else:
            # Cierre programático (por ejemplo después de login exitoso)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    login_window = LoginWindow()
    login_window.show() 
    
    sys.exit(app.exec_())
