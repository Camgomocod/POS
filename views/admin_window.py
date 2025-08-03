# views/admin_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget, QApplication, QMessageBox,
    QTabWidget, QScrollArea, QGridLayout, QSizePolicy,
    QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
from utils.colors import ColorPalette, CommonStyles
from controllers.auth_controller import AuthController
from views.user_management_window import UserManagementWidget
from datetime import datetime
import sys

class AdminDashboard(QWidget):
    """Panel principal de administración"""
    
    # Señales para acciones rápidas que navegan a las pestañas correspondientes
    manage_users = pyqtSignal()
    view_reports = pyqtSignal()
    manage_menu = pyqtSignal()
    open_settings = pyqtSignal()
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.auth_ctrl = AuthController()
        self.init_ui()
    
    def init_ui(self):
        """Configurar interfaz del dashboard"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 25, 30)
        layout.setSpacing(10)
        
        # Header con información del admin
        header = self.create_header()
        layout.addWidget(header)
        
        # Área de estadísticas rápidas
        self.stats_area = self.create_stats_area()
        layout.addWidget(self.stats_area)
        
        # Espaciador
        layout.addStretch()
    
    def update_stats(self):
        """Actualizar estadísticas del dashboard"""
        # Remover el área de estadísticas existente
        self.layout().removeWidget(self.stats_area)
        self.stats_area.deleteLater()
        
        # Crear nueva área de estadísticas
        self.stats_area = self.create_stats_area()
        self.layout().insertWidget(1, self.stats_area)
    
    def create_header(self):
        """Crear header del dashboard"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 {ColorPalette.YINMN_BLUE},
                           stop:1 {ColorPalette.OXFORD_BLUE});
                border-radius: 15px;
                padding: 5px;
            }}
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Información del admin
        info_layout = QVBoxLayout()
        
        welcome_label = QLabel(f"¡Bienvenido, {self.user.full_name}!")
        welcome_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {ColorPalette.PLATINUM};
        """)
        info_layout.addWidget(welcome_label)
        
        role_label = QLabel(f"🛡️ {self.user.role_display}")
        role_label.setStyleSheet(f"""
            font-size: 16px;
            color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.9)};
            font-weight: 500;
        """)
        info_layout.addWidget(role_label)
        
        last_login = self.user.last_login.strftime("%d/%m/%Y %H:%M") if self.user.last_login else "Primera vez"
        login_label = QLabel(f"🕐 Último acceso: {last_login}")
        login_label.setStyleSheet(f"""
            font-size: 13px;
            border-radius: 8px;
            color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.8)};
        """)
        info_layout.addWidget(login_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        return header_frame
    
    def create_stats_area(self):
        """Crear área de estadísticas"""
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        layout = QVBoxLayout(stats_frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        title = QLabel("📊 Estadísticas del Sistema")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 5px;
        """)
        layout.addWidget(title)
        
        # Grid de estadísticas
        stats_grid = QGridLayout()
        stats_grid.setSpacing(5)
        
        # Obtener estadísticas reales
        try:
            users = self.auth_ctrl.get_all_users()
            active_users = len([u for u in users if u.is_active])
            admin_users = len([u for u in users if u.role.name == 'ADMIN'])
            recent_logins = len([u for u in users if u.last_login and 
                               (datetime.now() - u.last_login).days <= 7])
        except Exception:
            active_users = 0
            admin_users = 0
            recent_logins = 0
        
        # Estadísticas actualizadas
        stats_data = [
            ("👥", "Usuarios Activos", str(active_users), ColorPalette.SUCCESS),
            ("�️", "Administradores", str(admin_users), ColorPalette.WARNING),
            ("�", "Accesos Recientes", str(recent_logins), ColorPalette.YINMN_BLUE),
            ("📈", "Sistema", "Funcionando", ColorPalette.SUCCESS)
        ]
        
        for i, (icon, title_text, value, color) in enumerate(stats_data):
            stat_widget = self.create_stat_widget(icon, title_text, value, color)
            row = i // 2
            col = i % 2
            stats_grid.addWidget(stat_widget, row, col)
        
        layout.addLayout(stats_grid)
        
        return stats_frame
    
    def create_stat_widget(self, icon, title, value, color):
        """Crear widget individual de estadística"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(color, 0.1)};
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 0px;
            }}
        """)
        # Layout horizontal dentro del frame
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 10, 15, 10)
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            color: {color};
        """)
        layout.addWidget(icon_label)
        # Información
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 12px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
            font-weight: 500;
        """)
        info_layout.addWidget(title_label)
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {color};
        """)
        info_layout.addWidget(value_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        return widget
    
    def create_action_button(self, icon, title, description):
        """Crear botón de acción"""
        button = QPushButton()
        button.setFixedHeight(80)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.05)};
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
                border-radius: 10px;
                padding: 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        
        # Layout interno del botón
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 28px;
            color: {ColorPalette.YINMN_BLUE};
        """)
        layout.addWidget(icon_label)
        
        # Información
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        info_layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"""
            font-size: 11px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
        """)
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout)
        
        # Establecer el layout en el botón
        widget = QWidget()
        widget.setLayout(layout)
        button.setLayout(QVBoxLayout())
        button.layout().addWidget(widget)
        
        return button

class AdminWindow(QMainWindow):
    """Ventana principal de administración"""
    
    # Señales
    logout_requested = pyqtSignal()
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        # Controlador de autenticación para gestionar usuarios
        self.auth_ctrl = AuthController()
        self.init_ui()
    
    def init_ui(self):
        """Configurar interfaz principal"""
        # Configuración de ventana
        self.setWindowTitle(f"🛡️ Panel de Administración - {self.user.full_name}")
        self.setMinimumSize(1000, 700)
        
        # Centrar ventana
        self.center_window()
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra superior
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Contenido principal usando tabs
        self.content_tabs = QTabWidget()
        self.content_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
            QTabBar::tab {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                color: {ColorPalette.RICH_BLACK};
                padding: 12px 30px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                min-width: 100px;
            }}
            QTabBar::tab:selected {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
            }}
            QTabBar::tab:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.7)};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        
        # Dashboard principal
        dashboard = AdminDashboard(self.user)
        # Conectar señales de acciones rápidas a navegación de pestañas
        dashboard.manage_users.connect(lambda: self.content_tabs.setCurrentIndex(1))
        dashboard.view_reports.connect(lambda: self.content_tabs.setCurrentIndex(2))
        dashboard.manage_menu.connect(lambda: self.content_tabs.setCurrentIndex(3))
        dashboard.open_settings.connect(lambda: self.content_tabs.setCurrentIndex(4))
        self.content_tabs.addTab(dashboard, "🏠 Dashboard")
        
        # Pestaña Usuarios funcional
        self.users_widget = UserManagementWidget(self.user)
        self.users_widget.user_updated.connect(self.refresh_user_stats)
        self.content_tabs.addTab(self.users_widget, "👥 Usuarios")
        # Otras pestañas placeholder
        placeholder_tabs = [
            ("📊", "Reportes", "Reportes y estadísticas"),
            ("🍽️", "Menú", "Gestión de productos y categorías"),
            ("⚙️", "Configuración", "Configuración del sistema")
        ]
        for icon, title, desc in placeholder_tabs:
            placeholder = self.create_placeholder_tab(icon, title, desc)
            self.content_tabs.addTab(placeholder, f"{icon} {title}")
        main_layout.addWidget(self.content_tabs)
        
        # Estilo general
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {ColorPalette.PLATINUM}; 
            }}
        """)
    
    def create_top_bar(self):
        """Crear barra superior"""
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 {ColorPalette.RICH_BLACK},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.9)});
                border-bottom: 2px solid {ColorPalette.YINMN_BLUE};
            }}
        """)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Logo y título
        title_layout = QHBoxLayout()
        
        logo_label = QLabel("🛡️")
        logo_label.setStyleSheet("""
            font-size: 24px;
            color: white;
        """)
        title_layout.addWidget(logo_label)
        
        title_label = QLabel("Panel de Administración")
        title_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {ColorPalette.PLATINUM};
            margin-left: 10px;
        """)
        title_layout.addWidget(title_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Información del usuario y logout
        user_layout = QHBoxLayout()
        user_layout.setSpacing(15)
        
        user_info = QLabel(f"👨‍💼 {self.user.full_name}")
        user_info.setStyleSheet(f"""
            color: {ColorPalette.PLATINUM};
            font-size: 14px;
            font-weight: 500;
        """)
        user_layout.addWidget(user_info)
        
        logout_btn = QPushButton("🚪 Cerrar Sesión")
        logout_btn.setFixedHeight(35)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 6px 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
            }}
        """)
        logout_btn.clicked.connect(self.handle_logout)
        user_layout.addWidget(logout_btn)
        
        layout.addLayout(user_layout)
        
        return top_bar
    
    def create_placeholder_tab(self, icon, title, description):
        """Crear tab placeholder para futuras funcionalidades"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Icono grande
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            font-size: 64px;
            color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.6)};
            margin-bottom: 20px;
        """)
        layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 10px;
        """)
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet(f"""
            font-size: 16px;
            color: {ColorPalette.SILVER_LAKE_BLUE};
            margin-bottom: 20px;
        """)
        layout.addWidget(desc_label)
        
        # Mensaje de desarrollo
        dev_label = QLabel("🚧 Esta funcionalidad está en desarrollo")
        dev_label.setAlignment(Qt.AlignCenter)
        dev_label.setStyleSheet(f"""
            font-size: 14px;
            color: {ColorPalette.WARNING};
            background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.1)};
            padding: 10px 20px;
            border-radius: 8px;
            border: 1px solid {ColorPalette.with_alpha(ColorPalette.WARNING, 0.3)};
        """)
        layout.addWidget(dev_label)
        
        return widget
    
    def refresh_user_stats(self):
        """Refrescar estadísticas de usuarios en el dashboard"""
        # Actualizar las estadísticas del dashboard
        if hasattr(self, 'users_widget'):
            dashboard_widget = self.content_tabs.widget(0)  # El dashboard es la primera pestaña
            if hasattr(dashboard_widget, 'update_stats'):
                dashboard_widget.update_stats()
    
    def center_window(self):
        """Centrar ventana en la pantalla"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def handle_logout(self):
        """Manejar cierre de sesión"""
        reply = QMessageBox.question(self, "Cerrar Sesión", 
                                   "¿Estás seguro de que deseas cerrar sesión?",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Emitir señal y cerrar esta ventana
            self.logout_requested.emit()
            self.close()
    