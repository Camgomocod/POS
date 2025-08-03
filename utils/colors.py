# utils/colors.py
"""
Paleta de colores centralizada para la aplicación POS
Paleta de colores sobria y profesional
"""

class ColorPalette:
    """Paleta de colores principal de la aplicación"""
    
    # Colores principales
    RICH_BLACK = "#0d1b2a"      # Negro rico para fondos oscuros
    OXFORD_BLUE = "#1b263b"     # Azul Oxford para elementos secundarios
    YINMN_BLUE = "#415a77"      # Azul YInMn para elementos principales
    SILVER_LAKE_BLUE = "#778da9" # Azul plateado para elementos intermedios
    PLATINUM = "#e0e1dd"        # Platino para fondos claros
    
    # Colores de estado (ajustados a la paleta)
    SUCCESS = "#2d5016"         # Verde oscuro para éxito
    WARNING = "#8b6914"         # Amarillo oscuro para advertencias
    ERROR = "#7d1128"           # Rojo oscuro para errores
    INFO = YINMN_BLUE          # Azul principal para información
    
    # Colores para estados de órdenes (más sobrios)
    ORDER_PENDING = "#6c757d"   # Gris para pendiente
    ORDER_PREPARING = YINMN_BLUE # Azul principal para preparando
    ORDER_READY = "#28a745"     # Verde para listo
    ORDER_DELIVERED = "#6c757d" # Gris para entregado
    ORDER_CANCELLED = ERROR     # Rojo oscuro para cancelado
    
    # Variaciones de transparencia
    @classmethod
    def with_alpha(cls, color, alpha):
        """Agregar transparencia a un color"""
        if color.startswith('#'):
            color = color[1:]
        return f"rgba({int(color[0:2], 16)}, {int(color[2:4], 16)}, {int(color[4:6], 16)}, {alpha})"
    
    # Gradientes comunes
    @classmethod
    def gradient_primary(cls):
        """Gradiente principal"""
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {cls.OXFORD_BLUE}, stop:1 {cls.YINMN_BLUE})"
    
    @classmethod
    def gradient_secondary(cls):
        """Gradiente secundario"""
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {cls.YINMN_BLUE}, stop:1 {cls.SILVER_LAKE_BLUE})"
    
    @classmethod
    def gradient_background(cls):
        """Gradiente para fondos principales"""
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {cls.RICH_BLACK}, stop:1 {cls.OXFORD_BLUE})"

# Estilos comunes reutilizables
class CommonStyles:
    """Estilos comunes para widgets"""
    
    @staticmethod
    def button_primary():
        """Estilo para botones principales"""
        return f"""
            QPushButton {{
                background-color: {ColorPalette.YINMN_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
            }}
            QPushButton:pressed {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
            QPushButton:disabled {{
                background-color: #6c757d;
                color: #adb5bd;
            }}
        """
    
    @staticmethod
    def button_secondary():
        """Estilo para botones secundarios"""
        return f"""
            QPushButton {{
                background-color: {ColorPalette.SILVER_LAKE_BLUE};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {ColorPalette.YINMN_BLUE};
            }}
            QPushButton:pressed {{
                background-color: {ColorPalette.OXFORD_BLUE};
            }}
        """
    
    @staticmethod
    def button_success():
        """Estilo para botones de éxito"""
        return f"""
            QPushButton {{
                background-color: {ColorPalette.SUCCESS};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #34641f;
            }}
            QPushButton:pressed {{
                background-color: #1e3a0d;
            }}
        """
    
    @staticmethod
    def button_warning():
        """Estilo para botones de advertencia"""
        return f"""
            QPushButton {{
                background-color: {ColorPalette.WARNING};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #a67c1a;
            }}
            QPushButton:pressed {{
                background-color: #6b4f0e;
            }}
        """
    
    @staticmethod
    def button_danger():
        """Estilo para botones de peligro"""
        return f"""
            QPushButton {{
                background-color: {ColorPalette.ERROR};
                color: {ColorPalette.PLATINUM};
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #9c1538;
            }}
            QPushButton:pressed {{
                background-color: #5c0e20;
            }}
        """
    
    @staticmethod
    def panel_main():
        """Estilo para paneles principales"""
        return f"""
            QFrame {{
                background-color: {ColorPalette.with_alpha(ColorPalette.PLATINUM, 0.95)};
                border-radius: 15px;
                border: 1px solid {ColorPalette.SILVER_LAKE_BLUE};
            }}
        """
    
    @staticmethod
    def input_field():
        """Estilo para campos de entrada"""
        return f"""
            QLineEdit, QSpinBox, QComboBox, QDateEdit {{
                background-color: {ColorPalette.PLATINUM};
                border: 2px solid {ColorPalette.SILVER_LAKE_BLUE};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: {ColorPalette.RICH_BLACK};
            }}
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus {{
                border-color: {ColorPalette.YINMN_BLUE};
            }}
        """
