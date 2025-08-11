# views/reports_view_simple.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from utils.colors import ColorPalette

class ReportsView(QWidget):
    switch_to_main = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        print("🔄 Inicializando ReportsView simplificado...")
        
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
        title_label = QLabel("📊 Reportes - Versión Simplificada")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Mensaje informativo
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.StyledPanel)
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {ColorPalette.PLATINUM};
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        info_layout = QVBoxLayout(info_frame)
        
        info_label = QLabel("🔧 Módulo de Reportes Deshabilitado")
        info_label.setFont(QFont("Arial", 16, QFont.Bold))
        info_label.setStyleSheet(f"color: {ColorPalette.RICH_BLACK}; margin-bottom: 10px;")
        info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)
        
        desc_label = QLabel(
            "El módulo de reportes ha sido simplificado para garantizar la estabilidad\n"
            "de la aplicación en Windows 11.\n\n"
            "Los gráficos y funcionalidades avanzadas han sido removidos para\n"
            "eliminar los conflictos con matplotlib.\n\n"
            "Esta versión se enfoca en la estabilidad del sistema principal."
        )
        desc_label.setStyleSheet(f"color: {ColorPalette.OXFORD_BLUE}; text-align: center;")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        main_layout.addWidget(info_frame)
        
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
            ("Estado:", "Base de datos vacía")
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
