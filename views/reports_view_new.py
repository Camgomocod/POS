# views/reports_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from utils.colors import ColorPalette

class ReportsView(QWidget):
    switch_to_main = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        print("🔄 Inicializando ReportsView...")
        self.init_ui()
        print("✅ ReportsView inicializado correctamente")

    def init_ui(self):
        """Inicializar la interfaz de usuario"""
        print("🎨 Configurando interfaz de reportes...")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título
        title_label = QLabel("📊 Reportes")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Métricas básicas
        metrics_frame = QFrame()
        metrics_frame.setFrameStyle(QFrame.StyledPanel)
        metrics_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        metrics_layout = QGridLayout(metrics_frame)
        
        # Mostrar métricas básicas estáticas
        labels = [
            ("Total Ventas:", "$0 COP"),
            ("Órdenes:", "0"),
            ("Ticket Promedio:", "$0 COP"),
            ("Estado:", "Sistema operativo")
        ]
        
        for i, (label_text, value_text) in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; font-weight: bold;")
            metrics_layout.addWidget(label, i, 0)
            
            value = QLabel(value_text)
            value.setStyleSheet(f"color: {ColorPalette.YINMN_BLUE}; font-size: 14px; font-weight: bold;")
            metrics_layout.addWidget(value, i, 1)
        
        main_layout.addWidget(metrics_frame)
        
        # Espaciador
        main_layout.addStretch()
        
        print("✅ Interfaz configurada")

    def refresh_data(self):
        """Método placeholder para compatibilidad"""
        pass
