# views/categories_management_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView, QAbstractItemView, QFrame, QLabel,
                             QLineEdit, QComboBox, QMenu, QAction, QApplication,
                             QDesktopWidget, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon
from utils.colors import ColorPalette
from controllers.menu_controller import MenuController
from models.category import Category

class CategoriesManagementView(QWidget):
    """Vista para gestión completa de categorías con operaciones CRUD"""
    
    # Señales
    category_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_ctrl = MenuController()
        self.parent_widget = parent
        
        # Detectar resolución de pantalla
        self.is_small_screen = self.detect_small_screen()
        
        self.init_ui()
        self.load_categories()
    
    def detect_small_screen(self):
        """Detectar si estamos en una pantalla pequeña"""
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry()
        
        # Considerar pantalla pequeña si width < 1500 o height < 800
        is_small = screen_geometry.width() < 1500 or screen_geometry.height() < 800
        
        if is_small:
            print(f"🔍 Pantalla pequeña detectada: {screen_geometry.width()}x{screen_geometry.height()}")
            print("📱 Aplicando modo compacto automático")
        
        return is_small
    
    def init_ui(self):
        """Configurar interfaz principal responsive sin header redundante"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Márgenes optimizados
        layout.setSpacing(10)  # Espaciado aumentado para mejor distribución
        
        # Filtros y búsqueda con más espacio
        filters_frame = self.create_filters_frame()
        layout.addWidget(filters_frame)
        
        # Tabla de categorías (expandible con scroll) - ahora ocupa más espacio
        table_frame = self.create_table_frame()
        layout.addWidget(table_frame, 1)  # Factor de expansión 1
        
        # Footer con información (altura fija mínima)
        footer_frame = self.create_footer()
        layout.addWidget(footer_frame)
        
        # Configurar tamaño mínimo optimizado sin header
        self.setMinimumSize(800, 450)  # Tamaño mínimo reducido sin header
        
        # Estilo general responsive
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
        """)
    
    def create_filters_frame(self):
        """Crear frame de filtros mejorado ocupando más espacio"""
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
        
        # Búsqueda por nombre con placeholder
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar categoría por nombre...")
        self.search_input.setFixedHeight(32)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                color: {ColorPalette.RICH_BLACK};
                min-width: 200px;
            }}
            QLineEdit:focus {{
                border-color: {ColorPalette.SUCCESS};
                background-color: white;
            }}
        """)
        self.search_input.textChanged.connect(self.filter_categories)
        layout.addWidget(self.search_input)
        
        # Filtro por estado con placeholder
        self.state_filter = QComboBox()
        self.state_filter.addItems(["🎯 Todas", "Activas", "Inactivas"])
        self.state_filter.setFixedHeight(32)
        self.state_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                color: {ColorPalette.RICH_BLACK};
                min-width: 100px;
            }}
            QComboBox:focus {{
                border-color: {ColorPalette.SUCCESS};
            }}
            QComboBox::drop-down {{
                border: none;
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 3px;
                width: 20px;
            }}
        """)
        self.state_filter.currentTextChanged.connect(self.filter_categories)
        layout.addWidget(self.state_filter)
        
        layout.addStretch()
        
        # Contador de resultados con más espacio
        self.results_label = QLabel("0 categorías")
        self.results_label.setStyleSheet(f"""
            font-size: 12px;
            font-weight: bold;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.7)};
            padding: 5px;
        """)
        layout.addWidget(self.results_label)
        
        return filters_frame
    
    def create_table_frame(self):
        """Crear frame expandido de la tabla ocupando más espacio"""
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
        
        # Tabla con scroll automático - ahora más prominente
        self.categories_table = QTableWidget()
        self.setup_responsive_table()
        layout.addWidget(self.categories_table)
        
        return table_frame
    
    def setup_responsive_table(self):
        """Configurar tabla responsive con scroll automático"""
        # Configurar columnas
        columns = ["ID", "Nombre", "Descripción", "Productos", "Estado", "Acciones"]
        self.categories_table.setColumnCount(len(columns))
        self.categories_table.setHorizontalHeaderLabels(columns)
        
        # Configurar propiedades de la tabla
        self.categories_table.setAlternatingRowColors(True)
        self.categories_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.categories_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.categories_table.setSortingEnabled(True)
        self.categories_table.verticalHeader().setVisible(False)
        
        # Configurar scroll automático
        self.categories_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.categories_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Configurar header con altura similar a productos
        header = self.categories_table.horizontalHeader()
        
        # Configurar altura del header
        header.setFixedHeight(45)
        header.setMinimumHeight(40)
        header.setMaximumHeight(50)
        
        # Configurar modos de redimensionamiento
        header.setSectionResizeMode(0, QHeaderView.Fixed)      # ID
        header.setSectionResizeMode(1, QHeaderView.Interactive) # Nombre
        header.setSectionResizeMode(2, QHeaderView.Stretch)    # Descripción (expandible)
        header.setSectionResizeMode(3, QHeaderView.Fixed)      # Productos
        header.setSectionResizeMode(4, QHeaderView.Fixed)      # Estado
        header.setSectionResizeMode(5, QHeaderView.Fixed)      # Acciones
        
        # Anchos optimizados según el tamaño de pantalla
        if self.is_small_screen:
            # Pantalla pequeña: columnas más compactas
            self.categories_table.setColumnWidth(0, 50)   # ID
            self.categories_table.setColumnWidth(1, 110)  # Nombre
            self.categories_table.setColumnWidth(3, 80)   # Productos
            self.categories_table.setColumnWidth(4, 80)   # Estado
            self.categories_table.setColumnWidth(5, 120)  # Acciones
            
            # Altura de filas más compacta
            self.categories_table.verticalHeader().setDefaultSectionSize(32)
        else:
            # Pantalla grande: columnas normales
            self.categories_table.setColumnWidth(0, 60)   # ID
            self.categories_table.setColumnWidth(1, 130)  # Nombre
            self.categories_table.setColumnWidth(3, 90)   # Productos
            self.categories_table.setColumnWidth(4, 90)   # Estado
            self.categories_table.setColumnWidth(5, 140)  # Acciones
            
            # Altura de filas normal
            self.categories_table.verticalHeader().setDefaultSectionSize(38)
        
        # Política de tamaño para permitir expansión
        from PyQt5.QtWidgets import QSizePolicy
        self.categories_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.categories_table.setMinimumHeight(200)  # Altura mínima
        
        # Estilo de la tabla responsive (unificado con productos)
        self.categories_table.setStyleSheet(f"""
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
        """)
    
    def create_footer(self):
        """Crear footer mejorado con más información"""
        footer_frame = QFrame()
        footer_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.8)};
                border-radius: 8px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                padding: 4px;
                max-height: 35px;
                min-height: 35px;
            }}
        """)
        
        layout = QHBoxLayout(footer_frame)
        layout.setContentsMargins(15, 6, 15, 6)
        
        # Información de estado mejorada
        self.status_label = QLabel("✅ Datos cargados correctamente")
        self.status_label.setStyleSheet(f"""
            font-size: 11px;
            color: {ColorPalette.SUCCESS};
            font-weight: bold;
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Información de última actualización mejorada
        self.last_update_label = QLabel("")
        self.last_update_label.setStyleSheet(f"""
            font-size: 11px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.6)};
        """)
        layout.addWidget(self.last_update_label)
        
        return footer_frame
    
    def load_categories(self):
        """Cargar categorías en la tabla"""
        try:
            # Mostrar estado de carga
            self.status_label.setText("🔄 Cargando categorías...")
            self.status_label.setStyleSheet(f"""
                font-size: 11px;
                color: {ColorPalette.WARNING};
                font-weight: bold;
            """)
            
            # Obtener categorías
            categories = self.menu_ctrl.get_all_categories(include_inactive=True)
            
            # Limpiar tabla
            self.categories_table.setRowCount(0)
            
            # Llenar tabla
            for category in categories:
                self.add_category_row(category)
            
            # Actualizar contador
            self.update_results_count()
            
            # Actualizar estado
            self.status_label.setText("✅ Datos cargados correctamente")
            self.status_label.setStyleSheet(f"""
                font-size: 11px;
                color: {ColorPalette.SUCCESS};
                font-weight: bold;
            """)
            
            # Actualizar timestamp
            from datetime import datetime
            self.last_update_label.setText(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error al cargar: {str(e)}")
            self.status_label.setStyleSheet(f"""
                font-size: 11px;
                color: {ColorPalette.ERROR};
                font-weight: bold;
            """)
            print(f"Error cargando categorías: {e}")
    
    def add_category_row(self, category):
        """Agregar fila de categoría a la tabla"""
        row = self.categories_table.rowCount()
        self.categories_table.insertRow(row)
        
        # ID
        id_item = QTableWidgetItem(str(category.id))
        id_item.setTextAlignment(Qt.AlignCenter)
        id_item.setFont(QFont("Arial", 11, QFont.Bold))
        id_item.setForeground(QColor(ColorPalette.SILVER_LAKE_BLUE))
        self.categories_table.setItem(row, 0, id_item)
        
        # Nombre
        name_item = QTableWidgetItem(category.name)
        name_item.setFont(QFont("Arial", 12, QFont.Bold))
        name_item.setForeground(QColor(ColorPalette.RICH_BLACK))
        self.categories_table.setItem(row, 1, name_item)
        
        # Descripción
        description = category.description or "Sin descripción"
        if len(description) > 50:
            description = description[:47] + "..."
        desc_item = QTableWidgetItem(description)
        desc_item.setFont(QFont("Arial", 11))
        desc_item.setForeground(QColor(ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.8)))
        desc_item.setToolTip(category.description or "Sin descripción")
        self.categories_table.setItem(row, 2, desc_item)
        
        # Productos (contar productos activos en esta categoría)
        try:
            products_count = len([p for p in category.products if p.is_active])
        except:
            products_count = 0
        
        products_item = QTableWidgetItem(str(products_count))
        products_item.setTextAlignment(Qt.AlignCenter)
        products_item.setFont(QFont("Arial", 11, QFont.Bold))
        products_item.setForeground(QColor(ColorPalette.YINMN_BLUE))
        self.categories_table.setItem(row, 3, products_item)
        
        # Estado
        status_text = "Activa" if category.is_active else "Inactiva"
        status_item = QTableWidgetItem(status_text)
        status_item.setTextAlignment(Qt.AlignCenter)
        status_item.setFont(QFont("Arial", 10, QFont.Bold))
        
        if category.is_active:
            status_item.setForeground(QColor(ColorPalette.SUCCESS))
        else:
            status_item.setForeground(QColor(ColorPalette.ERROR))
        
        self.categories_table.setItem(row, 4, status_item)
        
        # Acciones
        actions_widget = self.create_actions_widget(category)
        self.categories_table.setCellWidget(row, 5, actions_widget)
    
    def create_actions_widget(self, category):
        """Crear widget de acciones adaptado al tamaño de pantalla"""
        actions_frame = QFrame()
        actions_layout = QHBoxLayout(actions_frame)
        
        # Ajustar según el tamaño de pantalla
        if self.is_small_screen:
            actions_layout.setContentsMargins(1, 1, 1, 1)
            actions_layout.setSpacing(1)
            button_size = 25
            font_size = 11
        else:
            actions_layout.setContentsMargins(2, 1, 2, 1)
            actions_layout.setSpacing(2)
            button_size = 28
            font_size = 11
        
        # Botón editar adaptativo
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(button_size, button_size)
        edit_btn.setToolTip("Editar categoría")
        edit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 4px;
                font-size: {font_size}px;
                font-weight: bold;
                min-height: {button_size}px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """)
        edit_btn.clicked.connect(lambda: self.edit_category(category))
        actions_layout.addWidget(edit_btn)
        
        # Botón toggle estado adaptativo
        toggle_icon = "🔒" if category.is_active else "🔓"
        toggle_tooltip = "Desactivar" if category.is_active else "Activar"
        toggle_btn = QPushButton(toggle_icon)
        toggle_btn.setFixedSize(button_size, button_size)
        toggle_btn.setToolTip(toggle_tooltip)
        
        toggle_color = ColorPalette.WARNING if category.is_active else ColorPalette.SUCCESS
        toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {toggle_color};
                color: {ColorPalette.PLATINUM};
                border: none;
                border-radius: 4px;
                font-size: {font_size}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(toggle_color, 0.8)};
            }}
        """)
        toggle_btn.clicked.connect(lambda: self.toggle_category_status(category))
        actions_layout.addWidget(toggle_btn)
        
        # Botón eliminar adaptativo (solo si no tiene productos)
        products_count = len([p for p in getattr(category, 'products', []) if p.is_active])
        if products_count == 0:
            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(button_size, button_size)
            delete_btn.setToolTip("Eliminar categoría")
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ColorPalette.ERROR};
                    color: {ColorPalette.PLATINUM};
                    border: none;
                    border-radius: 4px;
                    font-size: {font_size}px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {ColorPalette.with_alpha(ColorPalette.ERROR, 0.8)};
                }}
            """)
            delete_btn.clicked.connect(lambda: self.delete_category(category))
            actions_layout.addWidget(delete_btn)
        
        return actions_frame
    
    def filter_categories(self):
        """Filtrar categorías según criterios de búsqueda"""
        search_text = self.search_input.text().lower()
        state_filter = self.state_filter.currentText()
        
        for row in range(self.categories_table.rowCount()):
            # Obtener datos de la fila
            name_item = self.categories_table.item(row, 1)
            desc_item = self.categories_table.item(row, 2)
            status_item = self.categories_table.item(row, 4)
            
            if name_item and desc_item and status_item:
                name = name_item.text().lower()
                description = desc_item.text().lower()
                status = status_item.text()
                
                # Filtro por texto
                text_match = (search_text in name or search_text in description)
                
                # Filtro por estado
                state_match = True
                if state_filter == "Activas":
                    state_match = status == "Activa"
                elif state_filter == "Inactivas":
                    state_match = status == "Inactiva"
                
                # Mostrar/ocultar fila
                show_row = text_match and state_match
                self.categories_table.setRowHidden(row, not show_row)
        
        # Actualizar contador
        self.update_results_count()
    
    def update_results_count(self):
        """Actualizar contador de resultados visibles"""
        visible_count = 0
        for row in range(self.categories_table.rowCount()):
            if not self.categories_table.isRowHidden(row):
                visible_count += 1
        
        total_count = self.categories_table.rowCount()
        self.results_label.setText(f"{visible_count} de {total_count} categorías")
    
    def create_category(self):
        """Crear nueva categoría - método mantenido para compatibilidad con header principal"""
        from views.menu_management_window import CategoryFormDialog
        
        dialog = CategoryFormDialog(self, is_edit=False)
        if dialog.exec_() == dialog.Accepted:
            self.load_categories()
            self.category_updated.emit()
    
    def edit_category(self, category):
        """Editar categoría existente"""
        from views.menu_management_window import CategoryFormDialog
        
        dialog = CategoryFormDialog(self, category=category, is_edit=True)
        if dialog.exec_() == dialog.Accepted:
            self.load_categories()
            self.category_updated.emit()
    
    def toggle_category_status(self, category):
        """Cambiar estado activo/inactivo de la categoría"""
        try:
            new_status = not category.is_active
            status_text = "activar" if new_status else "desactivar"
            
            reply = QMessageBox.question(
                self, 
                "Confirmar cambio",
                f"¿Está seguro que desea {status_text} la categoría '{category.name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success, message = self.menu_ctrl.update_category(
                    category.id,
                    name=category.name,
                    description=category.description,
                    is_active=new_status
                )
                
                if success:
                    QMessageBox.information(self, "Éxito", message)
                    self.load_categories()
                    self.category_updated.emit()
                else:
                    QMessageBox.warning(self, "Error", message)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
    
    def delete_category(self, category):
        """Eliminar categoría (solo si no tiene productos)"""
        try:
            # Verificar que no tenga productos activos
            products_count = len([p for p in getattr(category, 'products', []) if p.is_active])
            if products_count > 0:
                QMessageBox.warning(
                    self, 
                    "No se puede eliminar",
                    f"La categoría '{category.name}' tiene {products_count} producto(s) activo(s).\n"
                    "Debe eliminar o mover los productos antes de eliminar la categoría."
                )
                return
            
            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Está seguro que desea eliminar permanentemente la categoría '{category.name}'?\n\n"
                "Esta acción no se puede deshacer.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success, message = self.menu_ctrl.delete_category(category.id)
                
                if success:
                    QMessageBox.information(self, "Éxito", message)
                    self.load_categories()
                    self.category_updated.emit()
                else:
                    QMessageBox.warning(self, "Error", message)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
