class Config:
    # Base de datos
    DATABASE_URL = "sqlite:///data/pos.db"
    
    # Información del restaurante
    RESTAURANT_NAME = "FAST FOOD RESTAURANT"
    RESTAURANT_ADDRESS = "Calle Principal #123"
    RESTAURANT_PHONE = "Tel: (123) 456-7890"
    
    # Configuración de impresión
    PRINT_RECEIPT = True
    
    # Crear directorio de datos
    @staticmethod
    def init_directories():
        os.makedirs("data", exist_ok=True)

