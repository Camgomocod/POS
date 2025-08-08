from views.products_management_view import ProductsManagementView
from views.categories_management_view import CategoriesManagementView
from models.product import Product
from models.category import Category
from controllers.menu_controller import MenuController
from utils.colors import ColorPalette, CommonStyles
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from models.product import Product
from models.category import Category
from controllers.menu_controller import MenuController
from utils.colors import ColorPalette
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox,
                             QDialog, QFormLayout, QLineEdit, QTextEdit, QComboBox,
                             QCheckBox, QDialogButtonBox, QDoubleSpinBox, QSpinBox,
                             QFileDialog, QLabel, QGridLayout, QFrame, QHeaderView,
                             QAbstractItemView)
import os
import sys

class CategoryFormDialog(QDialog):
    """Diálogo para crear/editar categorías"""
    
    def __init__(self, parent=None, category=None, is_edit=False):
        super().__init__(parent)
        self.category = category
        self.is_edit = is_edit
        self.menu_ctrl = MenuController()
        self.init_ui()
    
    def init_ui(self):
        """Configurar interfaz del diálogo"""
        title = "Editar Categoría" if self.is_edit else "Nueva Categoría"
        self.setWindowTitle(title)
        self.setMinimumSize(400, 350)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Formulario
        form_frame = self.create_form()
        layout.addWidget(form_frame)
        
        # Botones
        buttons_frame = self.create_buttons()
        layout.addWidget(buttons_frame)
        
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
                           stop:0 {ColorPalette.SUCCESS},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)});
                border-radius: 10px;
                padding: 5px;
            }}
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(15, 10, 15, 10)
        
        icon = "✏️" if self.is_edit else "📁"
        title = "Editar Categoría" if self.is_edit else "Nueva Categoría"
        
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
                padding: 15px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
            }}
        """)
        
        layout = QFormLayout(form_frame)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Nombre
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("E.g., Bebidas, Postres, etc.")
        self.style_input(self.name_input)
        layout.addRow("📁 Nombre:", self.name_input)
        
        # Descripción
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Añade una descripción (opcional)")
        self.description_input.setFixedHeight(80)
        self.style_text_edit(self.description_input)
        layout.addRow("📝 Descripción:", self.description_input)
        
        # Estado (solo para edición)
        if self.is_edit:
            self.active_checkbox = QCheckBox("Categoría activa")
            self.style_checkbox(self.active_checkbox)
            layout.addRow("🔄 Estado:", self.active_checkbox)
        
        # Cargar datos si es edición
        if self.is_edit and self.category:
            self.load_category_data()
        
        return form_frame
    
    def style_input(self, widget):
        """Aplicar estilo a inputs"""
        widget.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.5)};
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                color: {ColorPalette.RICH_BLACK};
            }}
            QLineEdit:focus {{
                border-color: {ColorPalette.SUCCESS};
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.05)};
            }}
        """)
    
    def style_text_edit(self, widget):
        """Aplicar estilo a text edit"""
        widget.setStyleSheet(f"""
            QTextEdit {{
                padding: 8px 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.5)};
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                color: {ColorPalette.RICH_BLACK};
            }}
            QTextEdit:focus {{
                border-color: {ColorPalette.SUCCESS};
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.05)};
            }}
        """)
    
    def style_checkbox(self, widget):
        """Aplicar estilo a checkbox"""
        widget.setStyleSheet(f"""
            QCheckBox {{
                color: {ColorPalette.RICH_BLACK};
                font-weight: 500;
                font-size: 13px;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 4px;
                background-color: white;
            }}
            QCheckBox::indicator:checked {{
                border: 1px solid {ColorPalette.SUCCESS};
                border-radius: 4px;
                background-color: {ColorPalette.SUCCESS};
                image: url(icons/check.svg); 
            }}
        """)
    
    def create_buttons(self):
        """Crear botones de acción"""
        buttons_frame = QFrame()
        layout = QHBoxLayout(buttons_frame)
        layout.setSpacing(15)
        
        # Botón cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.setFixedHeight(38)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {ColorPalette.ERROR};
                border: 1px solid {ColorPalette.ERROR};
                padding: 8px 18px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
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
        save_text = "💾 Actualizar" if self.is_edit else "💾 Crear"
        save_btn = QPushButton(save_text)
        save_btn.setFixedHeight(38)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 18px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                min-width: 110px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.85)};
            }}
        """)
        save_btn.clicked.connect(self.save_category)
        layout.addWidget(save_btn)
        
        return buttons_frame
    
    def load_category_data(self):
        """Cargar datos de la categoría para edición"""
        self.name_input.setText(self.category.name)
        self.description_input.setPlainText(self.category.description or "")
        if hasattr(self, 'active_checkbox'):
            self.active_checkbox.setChecked(self.category.is_active)
    
    def save_category(self):
        """Guardar categoría"""
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "El nombre de la categoría es obligatorio")
            return
        
        try:
            if self.is_edit:
                is_active = self.active_checkbox.isChecked() if hasattr(self, 'active_checkbox') else True
                success, message = self.menu_ctrl.update_category(
                    self.category.id, name=name, description=description or None, is_active=is_active
                )
            else:
                success, message = self.menu_ctrl.create_category(name, description or None)
            
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class ProductFormDialog(QDialog):
    """Diálogo para crear/editar productos"""
    
    def __init__(self, parent=None, product=None, is_edit=False):
        super().__init__(parent)
        self.product = product
        self.is_edit = is_edit
        self.menu_ctrl = MenuController()
        self.init_ui()
    
    def init_ui(self):
        """Configurar interfaz del diálogo"""
        title = "Editar Producto" if self.is_edit else "Nuevo Producto"
        self.setWindowTitle(title)
        self.setMinimumSize(520, 560)  # reemplaza setFixedSize para permitir mejor auto-ajuste
        self.setModal(True)
        
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
        
        icon = "✏️" if self.is_edit else "🍽️"
        title = "Editar Producto" if self.is_edit else "Nuevo Producto"
        
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
        """Crear formulario (layout reorganizado)"""
        form_frame = QFrame()
        form_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
                padding: 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
            }}
        """)
        
        grid = QGridLayout(form_frame)
        grid.setContentsMargins(15, 15, 15, 15)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(10)
        
        def make_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet(f"""
                QLabel {{
                    font-size: 10px;
                    font-weight: 600;
                    color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.85)};
                    padding-left: 2px;
                }}
            """)
            return lbl
        
        # Nombre (fila 0)
        grid.addWidget(make_label("🍽️ Nombre del Producto"), 0, 0, 1, 4)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("E.g., Lomo Saltado, Torta de Chocolate...")
        self.style_input(self.name_input)
        grid.addWidget(self.name_input, 1, 0, 1, 4)
        
        # Categoría y Tiempo de preparación (fila 2)
        grid.addWidget(make_label("📁 Categoría"), 2, 0, 1, 2)
        grid.addWidget(make_label("⏱️ Tiempo de Preparación (min)"), 2, 2, 1, 2)
        
        self.category_combo = QComboBox()
        self.load_categories()
        self.style_combo(self.category_combo)
        grid.addWidget(self.category_combo, 3, 0, 1, 2)
        
        self.prep_time_input = QSpinBox()
        self.prep_time_input.setRange(0, 999)
        self.prep_time_input.setSuffix(" min")
        self.prep_time_input.setSpecialValueText("No especificado")
        self.style_spinbox(self.prep_time_input)
        grid.addWidget(self.prep_time_input, 3, 2, 1, 2)
        
        # Precio, Costo y Stock (fila 4)
        grid.addWidget(make_label("💰 Precio de Venta"), 4, 0)
        grid.addWidget(make_label("🏷️ Costo"), 4, 1)
        grid.addWidget(make_label("📦 Stock"), 4, 2, 1, 2)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 99999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("S/ ")
        self.style_spinbox(self.price_input)
        grid.addWidget(self.price_input, 5, 0)
        
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setRange(0.00, 99999.99)
        self.cost_input.setDecimals(2)
        self.cost_input.setPrefix("S/ ")
        self.cost_input.setSpecialValueText("No especificado")
        self.style_spinbox(self.cost_input)
        grid.addWidget(self.cost_input, 5, 1)
        
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 9999)
        self.stock_input.setSuffix(" unidades")
        self.stock_input.setSpecialValueText("Ilimitado")
        self.style_spinbox(self.stock_input)
        grid.addWidget(self.stock_input, 5, 2, 1, 2)
        
        # Descripción (fila 6)
        grid.addWidget(make_label("📝 Descripción"), 6, 0, 1, 4)
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Añade una descripción detallada del producto...")
        self.description_input.setMinimumHeight(80)
        self.description_input.setMaximumHeight(120)
        self.style_text_edit(self.description_input)
        grid.addWidget(self.description_input, 7, 0, 1, 4)
        
        # Ajustes de columnas para mejor proporción
        grid.setColumnStretch(0, 2) # Precio
        grid.setColumnStretch(1, 2) # Costo
        grid.setColumnStretch(2, 1) # Stock
        grid.setColumnStretch(3, 1) # Stock
        
        # Cargar datos si es edición
        if self.is_edit and self.product:
            self.load_product_data()
        
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
        """)
    
    def style_spinbox(self, widget):
        """Aplicar estilo a spinbox"""
        widget.setStyleSheet(f"""
            QSpinBox, QDoubleSpinBox {{
                padding: 10px 15px;
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
                font-size: 14px;
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
            }}
            QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """)
    
    def style_text_edit(self, widget):
        """Aplicar estilo a text edit"""
        widget.setStyleSheet(f"""
            QTextEdit {{
                padding: 10px 15px;
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 8px;
                font-size: 14px;
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
            }}
            QTextEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.05)};
            }}
        """)
    
    def style_checkbox(self, widget):
        """Aplicar estilo a checkbox"""
        widget.setStyleSheet(f"""
            QCheckBox {{
                color: {ColorPalette.RICH_BLACK};
                font-weight: 500;
                font-size: 14px;
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
                border: 2px solid {ColorPalette.YINMN_BLUE};
                border-radius: 4px;
                background-color: {ColorPalette.YINMN_BLUE};
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
        save_text = "💾 Actualizar" if self.is_edit else "💾 Crear"
        save_btn = QPushButton(save_text)
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.8)};
            }}
        """)
        save_btn.clicked.connect(self.save_product)
        layout.addWidget(save_btn)
        
        return buttons_frame
    
    def load_categories(self):
        """Cargar categorías en el combo"""
        if not hasattr(self, 'category_combo'):
            return
        self.category_combo.clear()
        try:
            categories = self.menu_ctrl.get_all_categories(include_inactive=self.is_edit)
            for category in categories:
                self.category_combo.addItem(category.name, category.id)
        except Exception as e:
            print(f"Error cargando categorías: {e}")
    
    def load_product_data(self):
        """Cargar datos del producto para edición"""
        self.name_input.setText(self.product.name)
        self.description_input.setPlainText(self.product.description or "")
        self.price_input.setValue(float(self.product.price))
        self.cost_input.setValue(float(self.product.cost) if self.product.cost else 0.0)
        self.prep_time_input.setValue(self.product.preparation_time or 0)
        self.stock_input.setValue(self.product.stock or 0)
        
        # Seleccionar categoría
        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == self.product.category_id:
                self.category_combo.setCurrentIndex(i)
                break
        
        # Solo cargar estado activo si estamos editando
        if hasattr(self, 'active_checkbox'):
            self.active_checkbox.setChecked(self.product.is_active)
    
    def save_product(self):
        """Guardar producto"""
        name = self.name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        price = self.price_input.value()
        cost = self.cost_input.value() if self.cost_input.value() > 0 else None
        prep_time = self.prep_time_input.value() if self.prep_time_input.value() > 0 else None
        stock = self.stock_input.value()
        category_id = self.category_combo.currentData()
        
        if not name:
            QMessageBox.warning(self, "Error", "El nombre del producto es obligatorio")
            return
        
        if not category_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar una categoría")
            return
        
        if price <= 0:
            QMessageBox.warning(self, "Error", "El precio debe ser mayor a cero")
            return
        
        try:
            if self.is_edit:
                is_active = self.active_checkbox.isChecked() if hasattr(self, 'active_checkbox') else True
                success, message = self.menu_ctrl.update_product(
                    self.product.id,
                    name=name,
                    description=description or None,
                    price=price,
                    cost=cost,
                    category_id=category_id,
                    preparation_time=prep_time,
                    stock=stock,
                    is_active=is_active
                    # Removido is_featured - se maneja automáticamente por el sistema
                )
            else:
                # Para productos nuevos, is_featured=False por defecto
                success, product, message = self.menu_ctrl.create_product(
                    name=name,
                    price=price,
                    category_id=category_id,
                    description=description or None,
                    cost=cost,
                    preparation_time=prep_time,
                    stock=stock
                    # Removido is_featured - el algoritmo decidirá después
                )
            
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class MenuManagementWidget(QWidget):
    """Widget principal de gestión de menú"""
    
    # Señales
    menu_updated = pyqtSignal()
    
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.menu_ctrl = MenuController()
        
        # Referencias a las vistas para poder actualizarlas
        self.categories_view = None
        self.products_view = None
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Configurar interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Contenido principal con tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                background-color: {ColorPalette.PLATINUM};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                font-size: 12px;
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                color: {ColorPalette.RICH_BLACK};
                padding: 6px 13px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                min-width: 100px
                min-height: 10px;
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
        
        # Pestaña Dashboard
        dashboard_tab = self.create_dashboard_tab()
        self.tabs.addTab(dashboard_tab, "📊 Dashboard")
        
        # Pestaña Categorías
        categories_tab = self.create_categories_tab()
        self.tabs.addTab(categories_tab, "📁 Categorías")
        
        # Pestaña Productos
        products_tab = self.create_products_tab()
        self.tabs.addTab(products_tab, "🍽️ Productos")
        
        layout.addWidget(self.tabs)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
        """)
    
    def create_header(self):
        """Crear header con título y botones"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                padding: 5px;
                max-height: 100px;
            }}
        """)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Título y descripción
        title_layout = QVBoxLayout()
        
        title_label = QLabel("🍽️ Gestión de Menú")
        title_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        title_layout.addWidget(title_label)
        
        desc_label = QLabel("Administra categorías, productos y analiza el rendimiento del menú")
        desc_label.setStyleSheet(f"""
            font-size: 13px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
        """)
        title_layout.addWidget(desc_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Botones de acción rápida
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        
        # Botón nueva categoría
        new_category_btn = QPushButton("📁 Nueva Categoría")
        new_category_btn.setFixedHeight(35)
        new_category_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)};
            }}
        """)
        new_category_btn.clicked.connect(self.create_category)
        buttons_layout.addWidget(new_category_btn)
        
        # Botón nuevo producto
        new_product_btn = QPushButton("🍽️ Nuevo Producto")
        new_product_btn.setFixedHeight(35)
        new_product_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.8)};
            }}
        """)
        new_product_btn.clicked.connect(self.create_product)
        buttons_layout.addWidget(new_product_btn)
        
        # Botón refrescar
        refresh_btn = QPushButton("🔄 Refrescar")
        refresh_btn.setFixedHeight(40)
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                color: {ColorPalette.SILVER_LAKE_BLUE};
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
            }}
        """)
        refresh_btn.clicked.connect(self.load_data)
        buttons_layout.addWidget(refresh_btn)
        
        layout.addLayout(buttons_layout)
        
        return header_frame
    
    def create_dashboard_tab(self):
        """Crear pestaña de dashboard"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Estadísticas generales
        stats_frame = self.create_stats_frame()
        layout.addWidget(stats_frame)
        
        # Productos más vendidos
        best_selling_frame = self.create_best_selling_frame()
        layout.addWidget(best_selling_frame)
        
        layout.addStretch()
        
        return widget
    
    def create_stats_frame(self):
        """Crear frame de estadísticas"""
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        layout = QVBoxLayout(stats_frame)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # Título
        title = QLabel("📊 Estadísticas del Menú")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        layout.addWidget(title)
        
        # Grid de estadísticas
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(8)
        layout.addLayout(self.stats_grid)
        
        return stats_frame
    
    def create_best_selling_frame(self):
        """Crear frame de productos más vendidos (compacto)"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 12px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(10)
        
        # Título
        title = QLabel("🏆 Top 2 Productos Más Vendidos")
        title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
            margin-bottom: 5px;
        """)
        layout.addWidget(title)
        
        # Contenedor para los productos
        self.products_container = QVBoxLayout()
        self.products_container.setSpacing(8)
        layout.addLayout(self.products_container)
        
        return frame
    
    def create_product_item(self, rank, product):
        """Crear item compacto de producto más vendido"""
        item_frame = QFrame()
        item_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.05)};
                border-radius: 8px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
                padding: 2px;
                min-height: 20px;
            }}
            QFrame:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.08)};
            }}
        """)
        
        layout = QHBoxLayout(item_frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)
        
        # Posición
        rank_label = QLabel(f"#{rank}")
        rank_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {ColorPalette.WARNING};
            min-width: 25px;
        """)
        layout.addWidget(rank_label)
        
        # Información del producto
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # Nombre
        name_label = QLabel(product.name)
        name_label.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 600;
            min-height: 20px;
            color: {ColorPalette.RICH_BLACK};
        """)
        info_layout.addWidget(name_label)
        
        # Detalles
        details = f"€{product.price:.2f} • {product.total_sold} vendidos • €{product.total_revenue:.2f} ingresos"
        details_label = QLabel(details)
        details_label.setStyleSheet(f"""
            font-size: 11px;
            min-height: 18px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
        """)
        info_layout.addWidget(details_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        return item_frame
    
    def create_categories_tab(self):
        """Crear pestaña de categorías"""
        from views.categories_management_view import CategoriesManagementView
        
        # Crear la vista de gestión de categorías y almacenar referencia
        self.categories_view = CategoriesManagementView(self)
        
        # Conectar señales para actualizar el dashboard cuando se modifiquen categorías
        self.categories_view.category_updated.connect(self.load_data)
        self.categories_view.category_updated.connect(self.menu_updated.emit)
        
        # Conectar señal para actualizar vista de productos cuando cambien categorías
        self.categories_view.category_updated.connect(self.update_products_view_from_categories)
        
        return self.categories_view

    def create_products_tab(self):
        """Crear pestaña de gestión de productos"""
        # Crear la vista de gestión de productos y almacenar referencia
        self.products_view = ProductsManagementView(self)
        self.products_view.product_updated.connect(self.load_data)
        self.products_view.product_updated.connect(self.menu_updated.emit)
        
        # Conectar señal para actualizar vista de categorías cuando cambien productos
        self.products_view.product_updated.connect(self.update_categories_view_from_products)
        
        return self.products_view
    
    def create_stat_widget(self, icon, title, value, color):
        """Crear widget individual de estadística compacto"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(color, 0.08)};
                border-left: 2px solid {color};
                border-radius: 6px;
                padding: 0px;
                min-height: 40px;
                max-height: 40px;
            }}
            QFrame:hover {{
                background-color: {ColorPalette.with_alpha(color, 0.12)};
            }}
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 12px;
            color: {color};
            min-width: 25px;
            min-height: 25px;
            position: relative;
        """)
        layout.addWidget(icon_label)
        
        # Información en línea
        info_text = f"{title}: {value}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet(f"""
            font-size: 12px;
            font-weight: 600;
            min-height: 25px;
            color: {ColorPalette.RICH_BLACK};
        """)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        return widget
    
    def load_data(self):
        """Cargar todos los datos"""
        self.load_stats()
        self.load_best_selling()
    
    def load_stats(self):
        """Cargar estadísticas del menú"""
        try:
            stats = self.menu_ctrl.get_menu_statistics()
            
            # Limpiar grid anterior
            for i in reversed(range(self.stats_grid.count())):
                self.stats_grid.itemAt(i).widget().setParent(None)
            
            # Crear widgets de estadísticas en una sola fila
            stats_data = [
                ("📁", "Categorías", str(stats['active_categories']), ColorPalette.SUCCESS),
                ("⭐", "Productos", str(stats['active_products']), ColorPalette.YINMN_BLUE),
                ("⭐", "Precio Mayor", f"€{stats['highest_price']:.2f}", ColorPalette.SILVER_LAKE_BLUE)
            ]
            
            for i, (icon, title, value, color) in enumerate(stats_data):
                stat_widget = self.create_stat_widget(icon, title, value, color)
                self.stats_grid.addWidget(stat_widget, 0, i)  # Todo en la fila 0
                
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
    
    def load_best_selling(self):
        """Cargar productos más vendidos"""
        try:
            best_selling = self.menu_ctrl.get_best_selling_products(limit=2)  # Solo los 2 primeros
            
            # Limpiar contenedor anterior
            for i in reversed(range(self.products_container.count())):
                child = self.products_container.itemAt(i).widget()
                if child:
                    child.setParent(None)
            
            # Agregar productos o mensaje si no hay datos
            if best_selling:
                for rank, product in enumerate(best_selling, 1):
                    product_item = self.create_product_item(rank, product)
                    self.products_container.addWidget(product_item)
            else:
                # Mensaje cuando no hay productos
                no_data_label = QLabel("📊 No hay datos de ventas disponibles")
                no_data_label.setStyleSheet(f"""
                    font-size: 13px;
                    color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.6)};
                    padding: 20px;
                    text-align: center;
                """)
                no_data_label.setAlignment(Qt.AlignCenter)
                self.products_container.addWidget(no_data_label)
                
        except Exception as e:
            print(f"Error cargando productos más vendidos: {e}")
    
    def create_category(self):
        """Crear nueva categoría"""
        dialog = CategoryFormDialog(self, is_edit=False)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
            self.menu_updated.emit()
            
            # Actualizar la tabla de categorías si está disponible
            if self.categories_view:
                self.categories_view.load_categories()
                
            # También actualizar la vista de productos para refrescar el filtro de categorías
            if self.products_view:
                self.products_view.load_filter_categories()
    
    def create_product(self):
        """Crear nuevo producto"""
        dialog = ProductFormDialog(self, is_edit=False)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
            self.menu_updated.emit()
            
            # Actualizar la tabla de productos si está disponible
            if self.products_view:
                self.products_view.load_products()
                
            # También actualizar la vista de categorías para refrescar el conteo de productos
            if self.categories_view:
                self.categories_view.load_categories()
    
    def update_categories_view_from_products(self):
        """Actualizar vista de categorías cuando cambien productos (para conteo de productos)"""
        if self.categories_view:
            self.categories_view.load_categories()
    
    def update_products_view_from_categories(self):
        """Actualizar vista de productos cuando cambien categorías (para filtro de categorías)"""
        if self.products_view:
            self.products_view.load_filter_categories()
