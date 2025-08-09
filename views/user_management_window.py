# views/user_management_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QComboBox, QMessageBox, QCheckBox,
    QGroupBox, QGridLayout, QSizePolicy, QSpacerItem, QTextEdit,
    QSplitter, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from utils.colors import ColorPalette, CommonStyles
from controllers.auth_controller import AuthController
from models.user import UserRole
import secrets

class UserFormDialog(QDialog):
    """Diálogo para crear/editar usuarios"""
    
    def __init__(self, parent=None, user=None, is_edit=False):
        super().__init__(parent)
        self.user = user
        self.is_edit = is_edit
        self.auth_ctrl = AuthController()
        self.init_ui()
    
    def init_ui(self):
        """Configurar interfaz del diálogo"""
        title = "Editar Usuario" if self.is_edit else "Nuevo Usuario"
        self.setWindowTitle(title)
        self.setFixedSize(450, 500)
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Formulario
        form_frame = self.create_form()
        layout.addWidget(form_frame)
        
        # Botones
        buttons_frame = self.create_buttons()
        layout.addWidget(buttons_frame)
        
        # Estilo general
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {ColorPalette.PLATINUM};
            }}
        """)
    
    def create_header(self):
        """Crear header del diálogo"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 {ColorPalette.YINMN_BLUE},
                           stop:1 {ColorPalette.OXFORD_BLUE});
                border-radius: 10px;
                padding: 5px;
            }}
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(15, 10, 15, 10)
        
        icon = "✏️" if self.is_edit else "👤"
        title = "Editar Usuario" if self.is_edit else "Crear Nuevo Usuario"
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            color: {ColorPalette.PLATINUM};
        """)
        layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {ColorPalette.PLATINUM};
            margin-left: 10px;
        """)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        return header_frame
    
    def create_form(self):
        """Crear formulario"""
        form_frame = QFrame()
        form_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
                padding: 10px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                max-width: 400px;
                border-radius: 4px;
            }}
        """)
        
        layout = QFormLayout(form_frame)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Campos del formulario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("nombre_usuario")
        self.style_input(self.username_input)
        layout.addRow("👤 Usuario:                   ", self.username_input)
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("Nombre completo")
        self.style_input(self.full_name_input)
        layout.addRow("📝 Nombre completo:", self.full_name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("correo@ejemplo.com (opcional)")
        self.style_input(self.email_input)
        layout.addRow("📧 Email:                       ", self.email_input)

        # Contraseña solo para nuevo usuario o si se quiere cambiar
        if not self.is_edit:    
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setPlaceholderText("Contraseña")
            self.style_input(self.password_input)
            layout.addRow("🔒 Contraseña:              ", self.password_input)
            
            # Botón generar contraseña
            generate_btn = QPushButton("🎲 Generar")
            generate_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.SILVER_LAKE_BLUE};
                    color: {ColorPalette.PLATINUM};
                    border: none;
                    padding: 8px 15px;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.8)};
                }}
            """)
            generate_btn.clicked.connect(self.generate_password)
            layout.addRow("", generate_btn)
        
        # Rol
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Usuario Regular", "Administrador"])
        self.style_combo(self.role_combo)
        layout.addRow("🛡️ Rol:                            ", self.role_combo)
        
        # Estado (solo para edición)
        if self.is_edit:
            self.active_checkbox = QCheckBox("Usuario activo")
            self.active_checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {ColorPalette.RICH_BLACK};
                    font-weight: 500;
                }}
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                }}
                QCheckBox::indicator:unchecked {{
                    border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                    border-radius: 4px;
                    background-color: {ColorPalette.PLATINUM};
                }}
                QCheckBox::indicator:checked {{
                    border: 2px solid {ColorPalette.SUCCESS};
                    border-radius: 4px;
                    background-color: {ColorPalette.SUCCESS};
                    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iMTAiIHZpZXdCb3g9IjAgMCAxMCAxMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTggM0w0LjUgNi41TDIgNCIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
                }}
            """)
            layout.addRow("🔄 Estado:", self.active_checkbox)
        
        # Cargar datos si es edición
        if self.is_edit and self.user:
            self.load_user_data()
        
        return form_frame
    
    def style_input(self, widget):
        """Aplicar estilo a inputs"""
        widget.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
                font-size: 14px;
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
            }}
            QLineEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.05)};
            }}
        """)
    
    def style_combo(self, widget):
        """Aplicar estilo a combobox"""
        widget.setStyleSheet(f"""
            QComboBox {{
                padding: 10px 15px;
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
                font-size: 14px;
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
                min-width: 150px;
            }}
            QComboBox:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {ColorPalette.RICH_BLACK};
            }}
        """)
    
    def create_buttons(self):
        """Crear botones de acción"""
        buttons_frame = QFrame()
        layout = QHBoxLayout(buttons_frame)
        layout.setSpacing(15)
        
        # Botón cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.1)};
                color: {ColorPalette.ERROR};
                border: 2px solid {ColorPalette.ERROR};
                padding: 8px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        layout.addStretch()
        
        # Botón guardar
        save_text = "💾 Actualizar" if self.is_edit else "💾 Crear Usuario"
        save_btn = QPushButton(save_text)
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        save_btn.clicked.connect(self.save_user)
        layout.addWidget(save_btn)
        
        return buttons_frame
    
    def generate_password(self):
        """Generar contraseña aleatoria"""
        password = secrets.token_urlsafe(12)
        self.password_input.setText(password)
        QMessageBox.information(self, "Contraseña Generada", 
                              f"Contraseña generada: {password}\n\nAsegúrate de guardarla en un lugar seguro.")
    
    def load_user_data(self):
        """Cargar datos del usuario para edición"""
        self.username_input.setText(self.user.username)
        self.full_name_input.setText(self.user.full_name)
        self.email_input.setText(self.user.email or "")
        self.role_combo.setCurrentIndex(0 if self.user.role == UserRole.REGULAR else 1)
        self.active_checkbox.setChecked(self.user.is_active)
    
    def save_user(self):
        """Guardar usuario"""
        # Validaciones
        username = self.username_input.text().strip()
        full_name = self.full_name_input.text().strip()
        email = self.email_input.text().strip() or None
        role = UserRole.REGULAR if self.role_combo.currentIndex() == 0 else UserRole.ADMIN
        
        if not username:
            QMessageBox.warning(self, "Error", "El nombre de usuario es obligatorio")
            return
        
        if not full_name:
            QMessageBox.warning(self, "Error", "El nombre completo es obligatorio")
            return
        
        # Validar formato de email si se proporciona
        if email and "@" not in email:
            QMessageBox.warning(self, "Error", "El formato del email no es válido")
            return
        
        # Validar duplicados
        user_id = self.user.id if self.is_edit else None
        is_valid, message = self.auth_ctrl.validate_user_data(username, email, user_id)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return
        
        if not self.is_edit:
            password = self.password_input.text()
            if not password:
                QMessageBox.warning(self, "Error", "La contraseña es obligatoria")
                return
            if len(password) < 4:
                QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 4 caracteres")
                return
        
        try:
            if self.is_edit:
                # Actualizar usuario existente
                is_active = self.active_checkbox.isChecked()
                success, message = self.auth_ctrl.update_user(
                    self.user.id,
                    username=username,
                    full_name=full_name,
                    email=email,
                    role=role,
                    is_active=is_active
                )
            else:
                # Crear nuevo usuario
                password = self.password_input.text()
                success, user, message = self.auth_ctrl.create_user(
                    username, password, full_name, email, role
                )
            
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class ResetPasswordDialog(QDialog):
    """Diálogo para resetear contraseña"""
    
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.auth_ctrl = AuthController()
        self.init_ui()
    
    def init_ui(self):
        """Configurar interfaz"""
        self.setWindowTitle("Resetear Contraseña")
        self.setFixedSize(400, 250)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 {ColorPalette.WARNING},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)});
                border-radius: 10px;
                padding: 5px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        icon_label = QLabel("🔑")
        icon_label.setStyleSheet("font-size: 20px; color: white;")
        icon_label.setFixedSize(40, 40)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(f"{self.user.full_name}")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white; margin-left: 10px;")
        header_layout.addWidget(title_label)
        
        layout.addWidget(header_frame)
        
        # Formulario
        form_frame = QFrame()
        form_layout = QFormLayout(form_frame)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Nueva contraseña")
        self.new_password_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
                font-size: 14px;
            }}  
            QLineEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
        form_layout.addRow("Cambio:", self.new_password_input)
        
        # Botón generar
        generate_btn = QPushButton("🎲 Generar Aleatoria")
        generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.8)};
            }}
        """)
        generate_btn.clicked.connect(self.generate_password)
        form_layout.addRow("", generate_btn)
        
        layout.addWidget(form_frame)
        
        # Botones
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.1)};
                color: {ColorPalette.ERROR};
                border: 2px solid {ColorPalette.ERROR};
                padding: 8px 20px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        
        reset_btn = QPushButton("🔑 Resetear")
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.WARNING};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 20px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)};
            }}
        """)
        reset_btn.clicked.connect(self.reset_password)
        buttons_layout.addWidget(reset_btn)
        
        layout.addWidget(buttons_frame)
        
        self.setStyleSheet(f"QDialog {{ background-color: {ColorPalette.PLATINUM}; }}")
    
    def generate_password(self):
        """Generar contraseña aleatoria"""
        password = secrets.token_urlsafe(12)
        self.new_password_input.setText(password)
    
    def reset_password(self):
        """Resetear contraseña"""
        new_password = self.new_password_input.text()
        
        if not new_password:
            QMessageBox.warning(self, "Error", "Debes ingresar una nueva contraseña")
            return
        
        try:
            success, message = self.auth_ctrl.update_user(self.user.id, password=new_password)
            
            if success:
                QMessageBox.information(self, "Éxito", 
                                      f"Contraseña de {self.user.full_name} actualizada correctamente.\n\n"
                                      f"Nueva contraseña: {new_password}")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class UserManagementWidget(QWidget):
    """Widget principal de gestión de usuarios"""
    
    # Señales
    user_updated = pyqtSignal()
    
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.auth_ctrl = AuthController()
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """Configurar interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header con título y botones
        header = self.create_header()
        layout.addWidget(header)
        
        # Área principal con tabla y panel de detalles
        main_area = self.create_main_area()
        layout.addWidget(main_area)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
        """)
    
    def create_header(self):
        """Crear header con título y botones"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 5px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                padding: 5px;
            }}
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título y descripción
        title_layout = QVBoxLayout()
        
        title_label = QLabel("👥 Gestión de Usuarios")
        title_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        title_layout.addWidget(title_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        
        # Botón refrescar
        refresh_btn = QPushButton("🔄 Refrescar")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 12px;
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                color: {ColorPalette.SILVER_LAKE_BLUE};
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                padding: 4px 10px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        refresh_btn.clicked.connect(self.load_users)
        buttons_layout.addWidget(refresh_btn)
        
        # Botón nuevo usuario
        new_user_btn = QPushButton("➕ Nuevo Usuario")
        new_user_btn.setFixedHeight(40)
        new_user_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        new_user_btn.clicked.connect(self.create_user)
        buttons_layout.addWidget(new_user_btn)
        
        layout.addLayout(buttons_layout)
        
        return header_frame
    
    def create_main_area(self):
        """Crear área principal con tabla y detalles"""
        splitter = QSplitter(Qt.Horizontal)
        
        # Tabla de usuarios
        table_frame = self.create_users_table()
        splitter.addWidget(table_frame)
        
        # Panel de detalles y acciones
        details_frame = self.create_details_panel()
        splitter.addWidget(details_frame)
        
        # Configurar tamaños
        splitter.setSizes([700, 300])
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                width: 2px;
            }}
        """)
        
        return splitter
    
    def create_users_table(self):
        """Crear tabla de usuarios"""
        table_frame = QFrame()
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        layout = QVBoxLayout(table_frame)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título de la tabla
        table_title = QLabel("📋 Lista de Usuarios")
        table_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 10px;
        """)
        layout.addWidget(table_title)
        
        # Tabla
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "Usuario", "Nombre Completo", "Email", "Rol", "Estado", "Último Acceso"
        ])
        
        # Configurar tabla
        self.users_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.users_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.users_table.setAlternatingRowColors(True)
        
        # Configurar header
        header = self.users_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # Ocultar encabezado vertical de índices
        self.users_table.verticalHeader().setVisible(False)
        
        # Estilo de la tabla
        self.users_table.setStyleSheet(f"""
            QTableWidget {{
                font-size: 13px;
                background-color: {ColorPalette.PLATINUM};
                gridline-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
                selection-background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
            }}
            QTableWidget::item {{
                font-size: 13px;
                padding: 12px 8px;
                border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
            }}
            QTableWidget::item:selected {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
                color: {ColorPalette.RICH_BLACK};
            }}
            QHeaderView::section {{
                font-size: 13px;
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                padding: 12px 8px;
                border: none;
                font-weight: bold;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 8px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 8px;
            }}
        """)
        
        # Conectar selección
        self.users_table.itemSelectionChanged.connect(self.on_user_selected)
        
        layout.addWidget(self.users_table)
        
        return table_frame
    
    def create_details_panel(self):
        """Crear panel de detalles del usuario"""
        details_frame = QFrame()
        details_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        layout = QVBoxLayout(details_frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("ℹ️ Detalles del Usuario")
        title_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 10px;
        """)
        layout.addWidget(title_label)
        
        # Información del usuario en área de scroll fija
        self.user_info_label = QLabel("Selecciona un usuario para ver los detalles")
        self.user_info_label.setWordWrap(True)
        self.user_info_label.setStyleSheet(f"""
            font-size: 13px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.6)};
            font-style: italic;
            padding: 20px;
            background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
            border-radius: 8px;
        """)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        scroll.setFixedHeight(200)
        scroll.setWidget(self.user_info_label)
        layout.addWidget(scroll)
        
        # Botones de acción
        actions_frame = QFrame()
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setSpacing(10)
        
        actions_title = QLabel("🔧 Acciones")
        actions_title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 5px;
        """)
        actions_layout.addWidget(actions_title)
        
        # Botón editar
        self.edit_btn = QPushButton("✏️ Editar Usuario")
        self.edit_btn.setEnabled(False)
        self.edit_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 12px;
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.8)};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)};
            }}
        """)
        self.edit_btn.clicked.connect(self.edit_user)
        actions_layout.addWidget(self.edit_btn)
        
        # Botón resetear contraseña
        self.reset_password_btn = QPushButton("🔑 Resetear Contraseña")
        self.reset_password_btn.setEnabled(False)
        self.reset_password_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 12px;
                background-color: {ColorPalette.WARNING};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)};
            }}
        """)
        self.reset_password_btn.clicked.connect(self.reset_password)
        actions_layout.addWidget(self.reset_password_btn)
        
        # Botón activar/desactivar
        self.toggle_status_btn = QPushButton("🔄 Cambiar Estado")
        self.toggle_status_btn.setEnabled(False)
        self.toggle_status_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 12px;
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.8)};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)};
            }}
        """)
        self.toggle_status_btn.clicked.connect(self.toggle_user_status)
        actions_layout.addWidget(self.toggle_status_btn)
        
        layout.addWidget(actions_frame)
        layout.addStretch()
        
        return details_frame
    
    def load_users(self):
        """Cargar usuarios en la tabla"""
        try:
            users = self.auth_ctrl.get_all_users()
            self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                # Usuario
                username_item = QTableWidgetItem(user.username)
                if not user.is_active:
                    username_item.setForeground(QColor(ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)))
                self.users_table.setItem(row, 0, username_item)
                
                # Nombre completo
                name_item = QTableWidgetItem(user.full_name)
                if not user.is_active:
                    name_item.setForeground(QColor(ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)))
                self.users_table.setItem(row, 1, name_item)
                
                # Email
                email_item = QTableWidgetItem(user.email or "")
                if not user.is_active:
                    email_item.setForeground(QColor(ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)))
                self.users_table.setItem(row, 2, email_item)
                
                # Rol
                role_item = QTableWidgetItem(user.role_display)
                if user.role == UserRole.ADMIN:
                    role_item.setForeground(QColor(ColorPalette.WARNING))
                else:
                    role_item.setForeground(QColor(ColorPalette.SILVER_LAKE_BLUE))
                self.users_table.setItem(row, 3, role_item)
                
                # Estado
                status_text = "🟢 Activo" if user.is_active else "🔴 Inactivo"
                status_item = QTableWidgetItem(status_text)
                status_item.setForeground(QColor(ColorPalette.SUCCESS if user.is_active else ColorPalette.ERROR))
                self.users_table.setItem(row, 4, status_item)
                
                # Último acceso
                last_login = user.last_login.strftime("%d/%m/%Y %H:%M") if user.last_login else "Nunca"
                login_item = QTableWidgetItem(last_login)
                if not user.is_active:
                    login_item.setForeground(QColor(ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)))
                self.users_table.setItem(row, 5, login_item)
                
                # Guardar referencia al usuario
                self.users_table.item(row, 0).setData(Qt.UserRole, user)
            
            # Ajustar ancho de todas las columnas excepto la última al contenido
            for col in range(self.users_table.columnCount() - 1):
                self.users_table.resizeColumnToContents(col)
            # Estirar la última columna (Último Acceso) para usar espacio restante
            self.users_table.horizontalHeader().setSectionResizeMode(
                self.users_table.columnCount() - 1, QHeaderView.Stretch
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar usuarios: {str(e)}")
    
    def on_user_selected(self):
        """Manejar selección de usuario"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            return
        # Obtener elemento de usuario y verificar
        user_item = self.users_table.item(current_row, 0)
        if not user_item:
            return
        user = user_item.data(Qt.UserRole)
        if not user:
            return
        # Mostrar detalles y habilitar acciones
        self.show_user_details(user)
        self.enable_action_buttons(user)
    
    def show_user_details(self, user):
        """Mostrar detalles del usuario"""
        status_color = ColorPalette.SUCCESS if user.is_active else ColorPalette.ERROR
        status_text = "Activo" if user.is_active else "Inactivo"
        last_login = user.last_login.strftime("%d/%m/%Y a las %H:%M") if user.last_login else "Nunca"
        created_date = user.created_at.strftime("%d/%m/%Y") if user.created_at else "Desconocida"
        
        details_html = f"""
        <div style="font-family: Arial; color: {ColorPalette.RICH_BLACK};">
            <h3 style="color: {ColorPalette.YINMN_BLUE}; margin-bottom: 15px;">
                👤 {user.full_name}
            </h3>
            
            <p><strong>🏷️ Usuario:</strong> {user.username}</p>
            
            <p><strong>📧 Email:</strong> {user.email or 'No especificado'}</p>
            
            <p><strong>🛡️ Rol:</strong> 
                <span style="color: {ColorPalette.WARNING if user.role == UserRole.ADMIN else ColorPalette.SILVER_LAKE_BLUE};">
                    {user.role_display}
                </span>
            </p>
            
            <p><strong>🔄 Estado:</strong> 
                <span style="color: {status_color}; font-weight: bold;">
                    {status_text}
                </span>
            </p>
            
            <p><strong>🕐 Último acceso:</strong> {last_login}</p>
        </div>
        """
        
        self.user_info_label.setText(details_html)
    
    def enable_action_buttons(self, user):
        """Habilitar botones de acción"""
        # No permitir editar el propio usuario si es el único admin
        can_edit = True
        if user.id == self.current_user.id and user.role == UserRole.ADMIN:
            # Verificar si es el único admin
            admins = [u for u in self.auth_ctrl.get_all_users() if u.role == UserRole.ADMIN and u.is_active]
            if len(admins) <= 1:
                can_edit = False
        
        self.edit_btn.setEnabled(can_edit)
        self.reset_password_btn.setEnabled(True)
        self.toggle_status_btn.setEnabled(can_edit)
        
        # Actualizar texto del botón de estado
        if user.is_active:
            self.toggle_status_btn.setText("🚫 Desactivar Usuario")
            self.toggle_status_btn.setStyleSheet(f"""
                QPushButton {{
                    font-size: 12px;
                    background-color: {ColorPalette.ERROR};
                    color: {ColorPalette.PLATINUM};
                    border: none;
                    padding: 10px 15px;
                    border-radius: 8px;
                    font-weight: bold;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
                }}
                QPushButton:disabled {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                    color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)};
                }}
            """)
        else:
            self.toggle_status_btn.setText("✅ Activar Usuario")
            self.toggle_status_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.SUCCESS};
                    color: {ColorPalette.PLATINUM};
                    border: none;
                    padding: 10px 15px;
                    border-radius: 8px;
                    font-weight: bold;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
                }}
                QPushButton:disabled {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                    color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)};
                }}
            """)
    
    def create_user(self):
        """Crear nuevo usuario"""
        dialog = UserFormDialog(self, is_edit=False)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()
            self.user_updated.emit()
    
    def edit_user(self):
        """Editar usuario seleccionado"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_item = self.users_table.item(current_row, 0)
            user = user_item.data(Qt.UserRole)
            
            dialog = UserFormDialog(self, user=user, is_edit=True)
            if dialog.exec_() == QDialog.Accepted:
                self.load_users()
                self.user_updated.emit()
    
    def reset_password(self):
        """Resetear contraseña del usuario seleccionado"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_item = self.users_table.item(current_row, 0)
            user = user_item.data(Qt.UserRole)
            
            dialog = ResetPasswordDialog(self, user=user)
            if dialog.exec_() == QDialog.Accepted:
                self.load_users()
                self.user_updated.emit()
    
    def toggle_user_status(self):
        """Cambiar estado del usuario (activar/desactivar)"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_item = self.users_table.item(current_row, 0)
            user = user_item.data(Qt.UserRole)
            
            action = "desactivar" if user.is_active else "activar"
            reply = QMessageBox.question(self, "Confirmar acción",
                                       f"¿Estás seguro de que deseas {action} al usuario {user.full_name}?",
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                try:
                    if user.is_active:
                        success, message = self.auth_ctrl.deactivate_user(user.id)
                    else:
                        success, message = self.auth_ctrl.activate_user(user.id)
                    
                    if success:
                        QMessageBox.information(self, "Éxito", message)
                        self.load_users()
                        self.user_updated.emit()
                    else:
                        QMessageBox.warning(self, "Error", message)
                        
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
