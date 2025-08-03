# main.py
import sys
from PyQt5.QtWidgets import QApplication
from views.pos_window import POSWindow
from utils.database import init_database

def main():
    # Inicializar base de datos
    print("🚀 Iniciando Sistema POS RestauranteFast...")
    print("📂 Inicializando base de datos...")
    init_database()
    print("✅ Base de datos lista")
    
    # Crear aplicación PyQt5
    app = QApplication(sys.argv)
    app.setApplicationName("POS RestauranteFast")
    app.setApplicationVersion("1.0")
    app.setStyle('Fusion')  # Estilo moderno
    
    # Crear y mostrar ventana principal
    print("🎨 Cargando interfaz principal...")
    window = POSWindow()
    window.show()
    print("✅ Sistema POS listo para usar!")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()