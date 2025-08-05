#!/usr/bin/env python3
"""
Sistema POS - Punto de Venta
Main entry point del sistema

Versión mejorada con manejo robusto de errores y señales
"""

import sys
import signal
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication

# Agregar directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.app_controller import AppController
from utils.database import init_database

# Definir códigos de color ANSI para terminal
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

def signal_handler(signum, frame):
    """Manejador de señales para salida limpia"""
    print(f"\n{Colors.YELLOW}🚨 Señal {signum} recibida. Cerrando aplicación...{Colors.RESET}")
    QApplication.quit()

def main():
    """Función principal del sistema POS"""
    
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print(f"{Colors.CYAN}🚀 Iniciando Sistema POS RestauranteFast...{Colors.RESET}")
    
    try:
        # Inicializar base de datos
        print(f"{Colors.BLUE}📂 Inicializando base de datos...{Colors.RESET}")
        init_database()
        print(f"{Colors.GREEN}✅ Base de datos lista{Colors.RESET}")
        
        # Configuraciones de alta resolución antes de crear la QApplication
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Crear aplicación PyQt5
        app = QApplication(sys.argv)
        app.setApplicationName("POS RestauranteFast")
        app.setApplicationVersion("2.0")
        app.setStyle('Fusion')  # Estilo moderno
        
        # Configurar aplicación para manejar Ctrl+C
        app.setQuitOnLastWindowClosed(True)
        
        print(f"{Colors.BLUE}🔐 Iniciando sistema de autenticación...{Colors.RESET}")
        
        # Crear controlador principal de la aplicación
        app_controller = AppController()
        
        # Asegurar que el controlador no se destruya
        app.app_controller = app_controller
        
        # Iniciar aplicación con login
        app_controller.start_application()
        
        print(f"{Colors.GREEN}✅ Sistema POS listo para usar!{Colors.RESET}")
        print(f"{Colors.CYAN}💡 Para salir use Ctrl+C o cierre la ventana{Colors.RESET}")
        
        # Ejecutar aplicación
        return app.exec_()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🚨 Interrupción por teclado detectada{Colors.RESET}")
        return 0
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error crítico en main: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        
        # Mostrar error al usuario si es posible
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error Crítico")
            msg.setText(f"Error en el sistema: {str(e)}")
            msg.setDetailedText(traceback.format_exc())
            msg.exec_()
        except:
            pass  # Si no se puede mostrar el diálogo, continuar
            
        return 1
    
    finally:
        print(f"{Colors.CYAN}🔄 Limpiando recursos...{Colors.RESET}")
        try:
            QApplication.quit()
        except:
            pass
        print(f"{Colors.GREEN}✅ Sistema POS cerrado correctamente{Colors.RESET}")

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)