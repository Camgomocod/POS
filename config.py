import os
from datetime import datetime

class Config:
    """Configuración centralizada de la aplicación"""
    
    # Base de datos
    DATABASE_URL = "sqlite:///data/pos.db"
    
    # Información del restaurante
    RESTAURANT_NAME = "RESTAURANTE FASTFOOD"
    RESTAURANT_ADDRESS = "Calle Principal #123, Popayán"
    RESTAURANT_PHONE = "Tel: (602) 123-4567"
    RESTAURANT_EMAIL = "info@restaurantefastfood.com"
    
    # Configuración de la aplicación
    APP_NAME = "POS RestauranteFast"
    APP_VERSION = "1.0.0"
    
    # Configuración de impresión
    PRINT_RECEIPT = True
    RECEIPT_WIDTH = 40  # Caracteres por línea
    
    # Configuración de interfaz
    from utils.colors import ColorPalette
    THEME_PRIMARY_COLOR = ColorPalette.YINMN_BLUE
    THEME_SECONDARY_COLOR = ColorPalette.OXFORD_BLUE
    
    # Configuración de actualizaciones
    AUTO_REFRESH_INTERVAL = 10000  # 10 segundos
    
    @staticmethod
    def init_directories():
        """Crear directorios necesarios"""
        directories = ['data', 'logs', 'temp']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def get_database_path():
        """Obtener ruta completa de la base de datos"""
        return os.path.abspath(Config.DATABASE_URL.replace('sqlite:///', ''))
    
    @staticmethod
    def log_info(message):
        """Log simple de información"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] INFO: {message}")