import sys
from PyQt5.QtWidgets import QApplication
from views.pos_window import POSWindow
from utils.database import init_database

def main():
    # Inicializar base de datos
    print("Inicializando base de datos...")
    init_database()
    
    # Crear aplicación
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    # Crear y mostrar ventana principal
    window = POSWindow()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
