# main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from controllers.app_controller import AppController
from utils.database import init_database

def main():
    # Inicializar base de datos
    print("🚀 Iniciando Sistema POS RestauranteFast...")
    print("📂 Inicializando base de datos...")
    init_database()
    print("✅ Base de datos lista")
    
    # Configuraciones de alta resolución antes de crear la QApplication
    from PyQt5.QtCore import QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Crear aplicación PyQt5
    app = QApplication(sys.argv)
    app.setApplicationName("POS RestauranteFast")
    app.setApplicationVersion("2.0")
    app.setStyle('Fusion')  # Estilo moderno
    
    print("🔐 Iniciando sistema de autenticación...")
    
    # Crear controlador principal de la aplicación
    app_controller = AppController()
    
    # Iniciar aplicación con login
    app_controller.start_application()
    
    print("✅ Sistema POS listo para usar!")
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()