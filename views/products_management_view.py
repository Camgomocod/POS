# views/products_management_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView, QAbstractItemView, QFrame, QLabel,
                             QLineEdit, QComboBox, QApplication, QDialog, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from utils.colors import ColorPalette
from controllers.menu_controller import MenuController

class ProductsManagementView(QWidget):
    """Vista para la gestión de productos con operaciones CRUD."""
    
    product_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_ctrl = MenuController()
        self.is_small_screen = self.detect_small_screen()
        self.init_ui()
        self.load_products()

    def detect_small_screen(self):
        """Detecta si la pantalla es pequeña."""
        screen_geometry = QApplication.desktop().screenGeometry()
        return screen_geometry.width() < 1500 or screen_geometry.height() < 800

    def init_ui(self):
        """Configura la interfaz de usuario principal."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        filters_frame = self.create_filters_frame()
        layout.addWidget(filters_frame)
        
        table_frame = self.create_table_frame()
        layout.addWidget(table_frame, 1)
        
        # footer_frame = self.create_footer()
        # layout.addWidget(footer_frame)
        
        self.setStyleSheet(f"background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};")

    def create_filters_frame(self):
        """Crea el marco para los filtros y la búsqueda."""
        filters_frame = QFrame()
        filters_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.8)};
                border-radius: 8px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                padding: 6px;
                max-height: 55px;
                min-height: 55px;
            }}
        """)
        
        layout = QHBoxLayout(filters_frame)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(15)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar producto por nombre...")
        self.search_input.setFixedHeight(32)
        self.search_input.setStyleSheet(CommonStyles.get_line_edit_style())
        self.search_input.textChanged.connect(self.filter_products)
        layout.addWidget(self.search_input)
        
        self.category_filter = QComboBox()
        self.load_filter_categories()
        self.category_filter.setFixedHeight(32)
        self.category_filter.setStyleSheet(CommonStyles.get_combo_box_style())
        self.category_filter.currentTextChanged.connect(self.filter_products)
        layout.addWidget(self.category_filter)

        self.state_filter = QComboBox()
        self.state_filter.addItems(["🎯 Todos", "Activos", "Inactivos"])
        self.state_filter.setFixedHeight(32)
        self.state_filter.setStyleSheet(CommonStyles.get_combo_box_style())
        self.state_filter.currentTextChanged.connect(self.filter_products)
        layout.addWidget(self.state_filter)
        
        layout.addStretch()
        
        self.results_label = QLabel("0 productos")
        self.results_label.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
            padding: 5px;
        """)
        layout.addWidget(self.results_label)
        
        return filters_frame

    def create_table_frame(self):
        """Crea el marco para la tabla de productos."""
        table_frame = QFrame()
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border-radius: 10px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                padding: 5px;
            }}
        """)
        layout = QVBoxLayout(table_frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        self.products_table = QTableWidget()
        self.setup_responsive_table()
        layout.addWidget(self.products_table)
        
        return table_frame

    def setup_responsive_table(self):
        """Configura la tabla de productos para que sea responsive."""
        columns = ["ID", "Nombre", "Categoría", "Precio", "Costo", "Stock", "Estado", "Acciones"]
        self.products_table.setColumnCount(len(columns))
        self.products_table.setHorizontalHeaderLabels(columns)
        
        # Configurar propiedades de la tabla
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.products_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.products_table.setSortingEnabled(True)
        self.products_table.verticalHeader().setVisible(False)
        
        # Configurar scroll automático
        self.products_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.products_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.products_table.setStyleSheet(CommonStyles.get_table_widget_style())
        
        # Configurar header con altura similar a categories

        
        header = self.products_table.horizontalHeader()
        
        header.setFixedHeight(45)
        header.setMinimumHeight(40)
        header.setMaximumHeight(50)
        
        header.setSectionResizeMode(0, QHeaderView.Fixed)      # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)    # Nombre (expandible)
        header.setSectionResizeMode(2, QHeaderView.Fixed)      # Categoría
        header.setSectionResizeMode(3, QHeaderView.Fixed)      # Precio
        header.setSectionResizeMode(4, QHeaderView.Fixed)      # Costo
        header.setSectionResizeMode(5, QHeaderView.Fixed)      # Stock
        header.setSectionResizeMode(6, QHeaderView.Fixed)      # Estado
        header.setSectionResizeMode(7, QHeaderView.Fixed)      # Acciones
        
        if self.is_small_screen:
            self.products_table.setColumnWidth(0, 50)   # ID
            self.products_table.setColumnWidth(2, 110)  # Categoría
            self.products_table.setColumnWidth(3, 85)   # Precio
            self.products_table.setColumnWidth(4, 85)   # Costo
            self.products_table.setColumnWidth(5, 80)   # Stock
            self.products_table.setColumnWidth(6, 80)   # Estado
            self.products_table.setColumnWidth(7, 120)  # Acciones
            self.products_table.verticalHeader().setDefaultSectionSize(32)
        else:
            self.products_table.setColumnWidth(0, 60)   # ID
            self.products_table.setColumnWidth(2, 130)  # Categoría
            self.products_table.setColumnWidth(3, 100)  # Precio
            self.products_table.setColumnWidth(4, 100)  # Costo
            self.products_table.setColumnWidth(5, 90)   # Stock
            self.products_table.setColumnWidth(6, 90)   # Estado
            self.products_table.setColumnWidth(7, 140)  # Acciones
            self.products_table.verticalHeader().setDefaultSectionSize(38)
        
        # Política de tamaño para permitir expansión
        self.products_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.products_table.setMinimumHeight(200)  # Altura mínima
            
    def load_products(self):
        """Carga los productos en la tabla."""
        try:
            products = self.menu_ctrl.get_all_products(include_inactive=True)
            self.products_table.setRowCount(0)
            for product in products:
                self.add_product_row(product)
            self.update_results_count()
        except Exception as e:
            print(f"Error al cargar productos: {e}")

    def add_product_row(self, product):
        """Añade una fila de producto a la tabla."""
        row = self.products_table.rowCount()
        self.products_table.insertRow(row)
        
        # ID, Nombre, Categoria, Precio, Costo, Stock, Estado
        self.products_table.setItem(row, 0, QTableWidgetItem(str(product.id)))
        self.products_table.setItem(row, 1, QTableWidgetItem(product.name))
        self.products_table.setItem(row, 2, QTableWidgetItem(product.category.name if product.category else "N/A"))
        self.products_table.setItem(row, 3, QTableWidgetItem(f"$ {product.price:.2f}"))
        self.products_table.setItem(row, 4, QTableWidgetItem(f"$ {product.cost:.2f}" if product.cost is not None else "N/A"))
        self.products_table.setItem(row, 5, QTableWidgetItem(str(product.stock) if product.stock is not None else "Ilimitado"))
        
        status_text = "Activo" if product.is_active else "Inactivo"
        status_item = QTableWidgetItem(status_text)
        status_item.setForeground(QColor(ColorPalette.SUCCESS if product.is_active else ColorPalette.ERROR))
        self.products_table.setItem(row, 6, status_item)

        actions_widget = self.create_actions_widget(product)
        self.products_table.setCellWidget(row, 7, actions_widget)

    def create_actions_widget(self, product):
        """Crea los botones de acción para cada producto."""
        actions_frame = QFrame()
        actions_layout = QHBoxLayout(actions_frame)
        actions_layout.setContentsMargins(1, 1, 1, 1)
        actions_layout.setSpacing(2)
        
        button_size = 28 if not self.is_small_screen else 25
        font_size = 11

        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(button_size, button_size)
        edit_btn.setToolTip("Editar producto")
        edit_btn.setStyleSheet(CommonStyles.get_button_style(ColorPalette.YINMN_BLUE, font_size=font_size))
        edit_btn.clicked.connect(lambda: self.edit_product(product))
        actions_layout.addWidget(edit_btn)

        toggle_btn = QPushButton("🔒" if product.is_active else "🔓")
        toggle_btn.setFixedSize(button_size, button_size)
        toggle_color = ColorPalette.WARNING if product.is_active else ColorPalette.SUCCESS
        toggle_btn.setStyleSheet(CommonStyles.get_button_style(toggle_color, font_size=font_size))
        toggle_btn.clicked.connect(lambda: self.toggle_product_status(product))
        actions_layout.addWidget(toggle_btn)

        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(button_size, button_size)
        delete_btn.setToolTip("Eliminar producto")
        delete_btn.setStyleSheet(CommonStyles.get_button_style(ColorPalette.ERROR, font_size=font_size))
        delete_btn.clicked.connect(lambda: self.delete_product(product))
        actions_layout.addWidget(delete_btn)
        
        return actions_frame

    def filter_products(self):
        """Filtra los productos en la tabla."""
        search_text = self.search_input.text().lower()
        category_filter = self.category_filter.currentText()
        state_filter = self.state_filter.currentText()

        for row in range(self.products_table.rowCount()):
            name = self.products_table.item(row, 1).text().lower()
            category = self.products_table.item(row, 2).text()
            status = self.products_table.item(row, 6).text()

            text_match = search_text in name
            category_match = (category_filter == "Todas las categorías" or category_filter == category)
            state_match = (state_filter == "🎯 Todos" or state_filter.startswith(status))
            
            self.products_table.setRowHidden(row, not (text_match and category_match and state_match))
        
        self.update_results_count()

    def update_results_count(self):
        """Actualiza el contador de resultados visibles."""
        visible_count = sum(1 for row in range(self.products_table.rowCount()) if not self.products_table.isRowHidden(row))
        self.results_label.setText(f"{visible_count} de {self.products_table.rowCount()} productos")

    def load_filter_categories(self):
        """Carga las categorías en el ComboBox de filtro."""
        self.category_filter.clear()
        self.category_filter.addItem("Todas las categorías")
        try:
            categories = self.menu_ctrl.get_all_categories()
            for category in categories:
                self.category_filter.addItem(category.name)
        except Exception as e:
            print(f"Error loading categories for filter: {e}")

    def edit_product(self, product):
        """Abre el diálogo para editar un producto."""
        from views.menu_management_window import ProductFormDialog
        dialog = ProductFormDialog(self, product=product, is_edit=True)
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()
            self.product_updated.emit()

    def toggle_product_status(self, product):
        """Cambia el estado de un producto (activo/inactivo)."""
        new_status = not product.is_active
        status_text = "activar" if new_status else "desactivar"
        reply = QMessageBox.question(self, "Confirmar", f"¿Seguro que desea {status_text} el producto '{product.name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            success, message = self.menu_ctrl.toggle_product_status(product.id)
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.load_products()
                self.product_updated.emit()
            else:
                QMessageBox.warning(self, "Error", message)

    def delete_product(self, product):
        """Elimina un producto."""
        reply = QMessageBox.question(self, "Confirmar Eliminación", 
                                     f"¿Está seguro de que desea eliminar '{product.name}'? Esta acción no se puede deshacer.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            success, message = self.menu_ctrl.delete_product(product.id)
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.load_products()
                self.product_updated.emit()
            else:
                QMessageBox.warning(self, "Error", message)

class CommonStyles:
    @staticmethod
    def get_line_edit_style():
        return f"""
            QLineEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px; padding: 6px 12px; font-size: 12px;
            }}
            QLineEdit:focus {{ border-color: {ColorPalette.SUCCESS}; }}
        """

    @staticmethod
    def get_combo_box_style():
        return f"""
            QComboBox {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px; padding: 6px 12px; font-size: 12px;
            }}
            QComboBox:focus {{ border-color: {ColorPalette.SUCCESS}; }}
            QComboBox::drop-down {{ border: none; }}
        """

    @staticmethod
    def get_table_widget_style():
        return f"""
            QTableWidget {{
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 6px;
                background-color: {ColorPalette.PLATINUM};
                gridline-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                selection-background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.2)};
                font-size: 11px;
            }}
            QTableWidget::item {{
                padding: 6px 3px;
                border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                color: {ColorPalette.RICH_BLACK};
            }}
            QTableWidget::item:selected {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.3)};
                color: {ColorPalette.RICH_BLACK};
            }}
            QTableWidget::item:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.1)};
            }}
            QHeaderView::section {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 {ColorPalette.SUCCESS},
                           stop:1 {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.8)});
                color: {ColorPalette.PLATINUM};
                padding: 8px 6px;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-right: 1px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.7)};
                height: 45px;
                min-height: 40px;
                max-height: 50px;
            }}
            QHeaderView::section:first {{
                border-top-left-radius: 4px;
            }}
            QHeaderView::section:last {{
                border-top-right-radius: 4px;
                border-right: none;
            }}
            QScrollBar:vertical {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
            QScrollBar:horizontal {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """

    @staticmethod
    def get_button_style(bg_color, text_color="white", font_size=11):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: 4px;
                font-size: {font_size}px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {ColorPalette.with_alpha(bg_color, 0.8)}; }}
        """
