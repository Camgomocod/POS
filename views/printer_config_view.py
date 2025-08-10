# views/printer_config_view.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QMessageBox, QApplication,
    QAbstractItemView, QHeaderView, QProgressBar, QTextEdit,
    QGroupBox, QFormLayout, QSpinBox, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor
from utils.colors import ColorPalette
from utils.printer import ThermalPrinter
import json
import os

class PrinterDetectionThread(QThread):
    """Thread para detectar impresoras sin bloquear la UI"""
    
    printers_found = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def run(self):
        try:
            printers = ThermalPrinter.get_available_printers()
            self.printers_found.emit(printers)
        except Exception as e:
            self.error_occurred.emit(str(e))

class PrinterConfigView(QWidget):
    """Vista para configurar impresoras térmicas USB"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.printer = ThermalPrinter()
        self.detection_thread = None
        self.init_ui()
        self.load_current_config()
    
    def init_ui(self):
        """Configurar interfaz de usuario"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Header compacto
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        title = QLabel("🖨️ Configuración de Impresora Térmica")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {ColorPalette.RICH_BLACK};
        """)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        desc = QLabel("Configure su impresora térmica USB de 57mm")
        desc.setStyleSheet(f"""
            font-size: 12px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.6)};
        """)
        desc.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(desc)
        
        main_layout.addLayout(header_layout)
        
        # Layout principal en dos columnas
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Columna izquierda: Configuración y Detección
        left_column = QVBoxLayout()
        left_column.setSpacing(10)
        
        current_config_group = self.create_current_config_section()
        left_column.addWidget(current_config_group)
        
        detection_group = self.create_detection_section()
        left_column.addWidget(detection_group)
        
        left_column.addStretch()
        
        # Columna derecha: Tabla de impresoras
        right_column = QVBoxLayout()
        table_group = self.create_printers_table_section()
        right_column.addWidget(table_group)
        
        # Agregar columnas al layout principal
        content_layout.addLayout(left_column, 1)  # 40% del ancho
        content_layout.addLayout(right_column, 2)  # 60% del ancho
        
        main_layout.addLayout(content_layout)
        
        # Configuración avanzada en una fila completa al final
        advanced_group = self.create_advanced_config_section()
        main_layout.addWidget(advanced_group)
        
        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
            }}
        """)
    
    def create_current_config_section(self):
        """Crear sección de configuración actual"""
        group = QGroupBox("⚙️ Estado Actual")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 13px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.3)};
                border-radius: 6px;
                margin-top: 8px;
                padding: 10px;
                background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.05)};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                background-color: {ColorPalette.PLATINUM};
                border-radius: 3px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Status compacto
        self.current_printer_label = QLabel("❌ Sin configurar")
        self.current_printer_label.setStyleSheet(f"""
            font-size: 11px;
            color: {ColorPalette.WARNING};
            padding: 8px;
            background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.1)};
            border-radius: 4px;
            border: 1px solid {ColorPalette.with_alpha(ColorPalette.WARNING, 0.2)};
        """)
        layout.addWidget(self.current_printer_label)
        
        # Botones compactos
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        
        self.test_btn = QPushButton("🧪 Test")
        self.test_btn.setFixedHeight(28)
        self.test_btn.setEnabled(False)
        self.test_btn.setStyleSheet(self.get_compact_button_style(ColorPalette.SUCCESS))
        self.test_btn.clicked.connect(self.test_printer)
        buttons_layout.addWidget(self.test_btn)
        
        self.clear_config_btn = QPushButton("🗑️ Limpiar")
        self.clear_config_btn.setFixedHeight(28)
        self.clear_config_btn.setEnabled(False)
        self.clear_config_btn.setStyleSheet(self.get_compact_button_style(ColorPalette.ERROR))
        self.clear_config_btn.clicked.connect(self.clear_configuration)
        buttons_layout.addWidget(self.clear_config_btn)
        
        layout.addLayout(buttons_layout)
        
        return group
    
    def create_detection_section(self):
        """Crear sección de detección de impresoras"""
        group = QGroupBox("🔍 Buscar USB")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 13px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
                border-radius: 6px;
                margin-top: 8px;
                padding: 10px;
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.05)};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                background-color: {ColorPalette.PLATINUM};
                border-radius: 3px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Información compacta
        info_label = QLabel("Busque impresoras USB conectadas")
        info_label.setStyleSheet(f"""
            font-size: 11px;
            color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.6)};
            padding: 6px;
            background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.1)};
            border-radius: 3px;
        """)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Botón y progreso compactos
        detection_layout = QVBoxLayout()
        detection_layout.setSpacing(5)
        
        self.detect_btn = QPushButton("🔄 Buscar")
        self.detect_btn.setFixedHeight(32)
        self.detect_btn.setStyleSheet(self.get_compact_button_style(ColorPalette.YINMN_BLUE))
        self.detect_btn.clicked.connect(self.detect_printers)
        detection_layout.addWidget(self.detect_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.3)};
                border-radius: 4px;
                background-color: {ColorPalette.PLATINUM};
            }}
            QProgressBar::chunk {{
                background-color: {ColorPalette.YINMN_BLUE};
                border-radius: 3px;
            }}
        """)
        detection_layout.addWidget(self.progress_bar)
        
        layout.addLayout(detection_layout)
        
        return group
    
    def create_printers_table_section(self):
        """Crear sección de tabla de impresoras"""
        group = QGroupBox("📋 Impresoras Disponibles")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 13px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 6px;
                margin-top: 8px;
                padding: 10px;
                background-color: {ColorPalette.PLATINUM};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                background-color: {ColorPalette.PLATINUM};
                border-radius: 3px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Tabla
        self.printers_table = QTableWidget()
        self.setup_printers_table()
        layout.addWidget(self.printers_table)
        
        return group
    
    def setup_printers_table(self):
        """Configurar tabla de impresoras"""
        self.printers_table.setColumnCount(5)
        self.printers_table.setHorizontalHeaderLabels([
            "Nombre", "Tipo", "USB", "Estado", "Acción"
        ])
        
        # Configurar propiedades
        self.printers_table.setAlternatingRowColors(True)
        self.printers_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.printers_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.printers_table.verticalHeader().setVisible(False)
        self.printers_table.setMinimumHeight(250)
        
        # Configurar header
        header = self.printers_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Nombre
        header.setSectionResizeMode(1, QHeaderView.Fixed)    # Tipo
        header.setSectionResizeMode(2, QHeaderView.Fixed)    # USB
        header.setSectionResizeMode(3, QHeaderView.Fixed)    # Estado
        header.setSectionResizeMode(4, QHeaderView.Fixed)    # Acción
        
        self.printers_table.setColumnWidth(1, 70)
        self.printers_table.setColumnWidth(2, 50)
        self.printers_table.setColumnWidth(3, 70)
        self.printers_table.setColumnWidth(4, 80)
        
        # Estilo compacto
        self.printers_table.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 4px;
                background-color: {ColorPalette.PLATINUM};
                gridline-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.2)};
                font-size: 11px;
            }}
            QHeaderView::section {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                padding: 6px;
                font-weight: bold;
                font-size: 11px;
                border: none;
                border-right: 1px solid {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.2)};
            }}
            QTableWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.1)};
            }}
            QTableWidget::item:selected {{
                background-color: {ColorPalette.with_alpha(ColorPalette.YINMN_BLUE, 0.2)};
            }}
        """)
    
    def create_advanced_config_section(self):
        """Crear sección de configuración avanzada"""
        group = QGroupBox("⚙️ Configuración")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 13px;
                font-weight: bold;
                color: {ColorPalette.RICH_BLACK};
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.WARNING, 0.3)};
                border-radius: 6px;
                margin-top: 8px;
                padding: 10px;
                background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.05)};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px 0 8px;
                background-color: {ColorPalette.PLATINUM};
                border-radius: 3px;
            }}
        """)
        
        # Layout horizontal para una sola fila
        main_layout = QHBoxLayout(group)
        main_layout.setSpacing(15)
        
        # Ancho de papel
        width_layout = QHBoxLayout()
        width_layout.setSpacing(5)
        
        width_label = QLabel("📏 Ancho:")
        width_label.setStyleSheet(f"font-size: 11px; color: {ColorPalette.RICH_BLACK};")
        width_layout.addWidget(width_label)
        
        self.paper_width_spinbox = QSpinBox()
        self.paper_width_spinbox.setRange(32, 48)
        self.paper_width_spinbox.setValue(42)
        self.paper_width_spinbox.setSuffix(" chars")
        self.paper_width_spinbox.setFixedWidth(90)
        self.paper_width_spinbox.setStyleSheet(self.get_compact_spinbox_style())
        width_layout.addWidget(self.paper_width_spinbox)
        
        main_layout.addLayout(width_layout)
        
        # Corte automático
        self.auto_cut_checkbox = QCheckBox("✂️ Corte automático")
        self.auto_cut_checkbox.setChecked(True)
        self.auto_cut_checkbox.setStyleSheet(f"""
            QCheckBox {{
                font-size: 11px;
                color: {ColorPalette.RICH_BLACK};
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.5)};
                border-radius: 3px;
                background-color: {ColorPalette.PLATINUM};
            }}
            QCheckBox::indicator:checked {{
                background-color: {ColorPalette.SUCCESS};
                border-color: {ColorPalette.SUCCESS};
            }}
        """)
        main_layout.addWidget(self.auto_cut_checkbox)
        
        # Espaciador
        main_layout.addStretch()
        
        # Botón guardar
        save_config_btn = QPushButton("💾 Guardar Configuración")
        save_config_btn.setFixedHeight(32)
        save_config_btn.setStyleSheet(self.get_compact_button_style(ColorPalette.SUCCESS))
        save_config_btn.clicked.connect(self.save_advanced_config)
        main_layout.addWidget(save_config_btn)
        
        return group
    
    def get_button_style(self, color):
        """Obtener estilo para botones"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(color, 0.8)};
            }}
            QPushButton:pressed {{
                background-color: {ColorPalette.with_alpha(color, 0.6)};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)};
            }}
        """
    
    def get_compact_button_style(self, color):
        """Obtener estilo compacto para botones"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(color, 0.8)};
            }}
            QPushButton:pressed {{
                background-color: {ColorPalette.with_alpha(color, 0.6)};
            }}
            QPushButton:disabled {{
                background-color: {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                color: {ColorPalette.with_alpha(ColorPalette.RICH_BLACK, 0.5)};
            }}
        """
    
    def get_spinbox_style(self):
        """Obtener estilo para spinbox"""
        return f"""
            QSpinBox {{
                padding: 8px 12px;
                border: 2px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 6px;
                font-size: 13px;
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
            }}
            QSpinBox:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """
    
    def get_compact_spinbox_style(self):
        """Obtener estilo compacto para spinbox"""
        return f"""
            QSpinBox {{
                padding: 4px 8px;
                border: 1px solid {ColorPalette.with_alpha(ColorPalette.SILVER_LAKE_BLUE, 0.3)};
                border-radius: 3px;
                font-size: 11px;
                background-color: {ColorPalette.PLATINUM};
                color: {ColorPalette.RICH_BLACK};
            }}
            QSpinBox:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """
    
    def detect_printers(self):
        """Detectar impresoras disponibles"""
        # Mostrar progreso
        self.detect_btn.setEnabled(False)
        self.detect_btn.setText("🔄 Buscando...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Progreso indeterminado
        
        # Limpiar tabla
        self.printers_table.setRowCount(0)
        
        # Crear y ejecutar thread de detección
        self.detection_thread = PrinterDetectionThread()
        self.detection_thread.printers_found.connect(self.on_printers_found)
        self.detection_thread.error_occurred.connect(self.on_detection_error)
        self.detection_thread.start()
    
    def on_printers_found(self, printers):
        """Manejar impresoras encontradas"""
        # Ocultar progreso
        self.progress_bar.setVisible(False)
        self.detect_btn.setEnabled(True)
        self.detect_btn.setText("🔄 Buscar Impresoras")
        
        if not printers:
            self.show_no_printers_message()
            return
        
        # Filtrar solo impresoras USB
        usb_printers = [p for p in printers if p.get('connection', '').lower() == 'usb']
        
        if not usb_printers:
            self.show_no_usb_printers_message()
            return
        
        # Llenar tabla
        for printer in usb_printers:
            self.add_printer_to_table(printer)
        
        # Mostrar resultado
        QMessageBox.information(
            self,
            "✅ Búsqueda Completada",
            f"Se encontraron {len(usb_printers)} impresoras USB.\n"
            f"Impresoras térmicas detectadas: {sum(1 for p in usb_printers if p.get('type') == 'thermal')}"
        )
    
    def on_detection_error(self, error_msg):
        """Manejar error en detección"""
        self.progress_bar.setVisible(False)
        self.detect_btn.setEnabled(True)
        self.detect_btn.setText("🔄 Buscar Impresoras")
        
        QMessageBox.critical(
            self,
            "❌ Error de Detección",
            f"Error al buscar impresoras:\n{error_msg}"
        )
    
    def show_no_printers_message(self):
        """Mostrar mensaje cuando no se encuentran impresoras"""
        self.printers_table.setRowCount(1)
        self.printers_table.setItem(0, 0, QTableWidgetItem("❌ No se encontraron impresoras"))
        self.printers_table.setSpan(0, 0, 1, 5)
        
        QMessageBox.information(
            self,
            "📭 Sin Resultados",
            "No se encontraron impresoras conectadas.\n\n"
            "Verifique que:\n"
            "• La impresora esté encendida\n"
            "• El cable USB esté conectado\n"
            "• Los drivers estén instalados"
        )
    
    def show_no_usb_printers_message(self):
        """Mostrar mensaje cuando no se encuentran impresoras USB"""
        self.printers_table.setRowCount(1)
        self.printers_table.setItem(0, 0, QTableWidgetItem("🔌 No se encontraron impresoras USB"))
        self.printers_table.setSpan(0, 0, 1, 5)
        
        QMessageBox.information(
            self,
            "🔌 Sin Impresoras USB",
            "No se encontraron impresoras conectadas por USB.\n\n"
            "Esta versión solo soporta impresoras USB.\n"
            "Verifique la conexión USB de su impresora térmica."
        )
    
    def add_printer_to_table(self, printer):
        """Agregar impresora a la tabla"""
        row = self.printers_table.rowCount()
        self.printers_table.insertRow(row)
        
        # Nombre
        name_item = QTableWidgetItem(printer['name'])
        self.printers_table.setItem(row, 0, name_item)
        
        # Tipo
        type_icon = "🖨️" if printer['type'] == 'thermal' else "🖥️"
        type_item = QTableWidgetItem(f"{type_icon} {printer['type'].title()}")
        if printer['type'] == 'thermal':
            type_item.setBackground(QColor(ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.2)))
            type_item.setForeground(QColor(ColorPalette.SUCCESS))
        self.printers_table.setItem(row, 1, type_item)
        
        # Conexión
        connection_item = QTableWidgetItem("🔌")
        connection_item.setForeground(QColor(ColorPalette.YINMN_BLUE))
        self.printers_table.setItem(row, 2, connection_item)
        
        # Estado
        status_icon = "🟢" if printer['status'] == 'available' else "🔴"
        status_item = QTableWidgetItem(f"{status_icon} {printer['status'].title()}")
        status_color = ColorPalette.SUCCESS if printer['status'] == 'available' else ColorPalette.ERROR
        status_item.setForeground(QColor(status_color))
        self.printers_table.setItem(row, 3, status_item)
        
        # Botón seleccionar
        select_btn = QPushButton("📌")
        select_btn.setToolTip("Seleccionar esta impresora")
        select_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ColorPalette.WARNING};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.8)};
            }}
        """)
        
        # Conectar señal
        select_btn.clicked.connect(
            lambda checked, name=printer['name']: self.select_printer(name)
        )
        self.printers_table.setCellWidget(row, 4, select_btn)
    
    def select_printer(self, printer_name):
        """Seleccionar impresora"""
        reply = QMessageBox.question(
            self,
            "🖨️ Confirmar Selección",
            f"¿Configurar '{printer_name}' como impresora de recibos?\n\n"
            f"Esta impresora se usará para imprimir todos los recibos del sistema.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Guardar configuración
                config_saved = self.printer.save_config(
                    printer_name=printer_name,
                    connection_type="usb",
                    paper_width=self.paper_width_spinbox.value(),
                    auto_cut=self.auto_cut_checkbox.isChecked()
                )
                
                if config_saved:
                    self.load_current_config()
                    QMessageBox.information(
                        self,
                        "✅ Configuración Guardada",
                        f"Impresora '{printer_name}' configurada correctamente.\n\n"
                        f"Ahora puede imprimir recibos desde el sistema POS."
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "❌ Error",
                        "No se pudo guardar la configuración de la impresora."
                    )
                    
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "❌ Error",
                    f"Error al configurar impresora:\n{str(e)}"
                )
    
    def load_current_config(self):
        """Cargar configuración actual"""
        try:
            # Recargar configuración
            self.printer.load_config()
            
            if self.printer.printer_name:
                # Hay impresora configurada
                self.current_printer_label.setText(
                    f"✅ {self.printer.printer_name[:25]}{'...' if len(self.printer.printer_name) > 25 else ''}\n"
                    f"🔌 {self.printer.connection_type.upper()} | 📏 {self.printer.paper_width}ch | ✂️ {'Sí' if getattr(self.printer, 'auto_cut', True) else 'No'}"
                )
                self.current_printer_label.setStyleSheet(f"""
                    font-size: 11px;
                    color: {ColorPalette.SUCCESS};
                    font-weight: bold;
                    padding: 8px;
                    background-color: {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.1)};
                    border-radius: 4px;
                    border: 1px solid {ColorPalette.with_alpha(ColorPalette.SUCCESS, 0.3)};
                    line-height: 1.3;
                """)
                
                # Habilitar botones
                self.test_btn.setEnabled(True)
                self.clear_config_btn.setEnabled(True)
                
                # Actualizar controles avanzados
                self.paper_width_spinbox.setValue(self.printer.paper_width)
                self.auto_cut_checkbox.setChecked(getattr(self.printer, 'auto_cut', True))
                
            else:
                # No hay impresora configurada
                self.current_printer_label.setText("❌ Sin configurar")
                self.current_printer_label.setStyleSheet(f"""
                    font-size: 11px;
                    color: {ColorPalette.WARNING};
                    font-weight: bold;
                    padding: 8px;
                    background-color: {ColorPalette.with_alpha(ColorPalette.WARNING, 0.1)};
                    border-radius: 4px;
                    border: 1px solid {ColorPalette.with_alpha(ColorPalette.WARNING, 0.2)};
                """)
                
                # Deshabilitar botones
                self.test_btn.setEnabled(False)
                self.clear_config_btn.setEnabled(False)
                
        except Exception as e:
            self.current_printer_label.setText(f"❌ Error: {str(e)}")
    
    def test_printer(self):
        """Probar impresión"""
        try:
            # Mostrar progreso
            progress_msg = QMessageBox(self)
            progress_msg.setWindowTitle("🖨️ Imprimiendo...")
            progress_msg.setText("Enviando página de prueba a la impresora...")
            progress_msg.setStandardButtons(QMessageBox.NoButton)
            progress_msg.show()
            QApplication.processEvents()
            
            # Intentar imprimir
            success = self.printer.test_print()
            
            progress_msg.close()
            
            if success:
                QMessageBox.information(
                    self,
                    "✅ Prueba Exitosa",
                    "La página de prueba se envió correctamente.\n\n"
                    "Verifique que se haya impreso en la impresora térmica.\n"
                    "Si no se imprimió, revise la conexión y configuración."
                )
            else:
                QMessageBox.warning(
                    self,
                    "❌ Error de Impresión",
                    "No se pudo imprimir la página de prueba.\n\n"
                    "Verifique que:\n"
                    "• La impresora esté encendida\n"
                    "• Tenga papel disponible\n"
                    "• La conexión USB esté activa\n"
                    "• Los drivers estén instalados"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Error",
                f"Error al probar impresora:\n{str(e)}"
            )
    
    def clear_configuration(self):
        """Limpiar configuración"""
        reply = QMessageBox.question(
            self,
            "🗑️ Confirmar",
            "¿Está seguro de que desea eliminar la configuración de impresora?\n\n"
            "No se podrán imprimir recibos hasta configurar una nueva impresora.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Eliminar archivo de configuración
                if os.path.exists(self.printer.config_file):
                    os.remove(self.printer.config_file)
                
                # Recargar configuración
                self.load_current_config()
                
                QMessageBox.information(
                    self,
                    "✅ Configuración Eliminada",
                    "La configuración de impresora ha sido eliminada.\n"
                    "Configure una nueva impresora para poder imprimir recibos."
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "❌ Error",
                    f"Error al eliminar configuración:\n{str(e)}"
                )
    
    def save_advanced_config(self):
        """Guardar configuración avanzada"""
        if not self.printer.printer_name:
            QMessageBox.warning(
                self,
                "⚠️ Sin Impresora",
                "Primero debe seleccionar una impresora antes de guardar la configuración avanzada."
            )
            return
        
        try:
            # Actualizar configuración
            config_saved = self.printer.save_config(
                printer_name=self.printer.printer_name,
                connection_type=self.printer.connection_type,
                paper_width=self.paper_width_spinbox.value(),
                auto_cut=self.auto_cut_checkbox.isChecked()
            )
            
            if config_saved:
                self.load_current_config()
                QMessageBox.information(
                    self,
                    "✅ Configuración Guardada",
                    "La configuración avanzada ha sido guardada correctamente."
                )
            else:
                QMessageBox.warning(
                    self,
                    "❌ Error",
                    "No se pudo guardar la configuración avanzada."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Error",
                f"Error al guardar configuración:\n{str(e)}"
            )
