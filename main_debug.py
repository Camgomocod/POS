#!/usr/bin/env python3
"""
Sistema POS - Punto de Venta
Versión con diagnóstico mejorado para Windows 11

Para depuración, ejecutar con: python main.py --debug
"""

import sys
import signal
import os
import platform
import argparse
from pathlib import Path

# Configurar argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Sistema POS RestauranteFast')
parser.add_argument('--debug', action='store_true', help='Modo debug con información detallada')
parser.add_argument('--no-gui', action='store_true', help='Modo sin GUI para testing')
args = parser.parse_args()

# Configurar nivel de debug
DEBUG_MODE = args.debug

def debug_print(message):
    """Imprimir mensaje solo en modo debug"""
    if DEBUG_MODE:
        print(f"🐛 DEBUG: {message}")

# Verificaciones previas específicas para Windows
if platform.system() == "Windows":
    debug_print("Detectado sistema Windows")
    
    # Configurar variables de entorno para Qt en Windows
    if not os.environ.get('QT_QPA_PLATFORM'):
        os.environ['QT_QPA_PLATFORM'] = 'windows'
        debug_print("Configurada variable QT_QPA_PLATFORM=windows")
    
    if not os.environ.get('QT_AUTO_SCREEN_SCALE_FACTOR'):
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
        debug_print("Configurada variable QT_AUTO_SCREEN_SCALE_FACTOR=1")

# Verificar que estamos en el directorio correcto
project_root = Path(__file__).parent.absolute()
if not (project_root / "requirements.txt").exists():
    print("❌ Error: No se encontró requirements.txt. ¿Estás en el directorio del proyecto?")
    sys.exit(1)

# Agregar directorio raíz al path
sys.path.insert(0, str(project_root))
debug_print(f"Directorio del proyecto: {project_root}")

# Verificar Python y paquetes críticos antes de importar PyQt5
def verify_environment():
    """Verificar entorno antes de ejecutar la aplicación"""
    debug_print("Verificando entorno de ejecución...")
    
    # Verificar versión de Python
    if sys.version_info < (3, 7):
        print(f"❌ Error: Se requiere Python 3.7+. Versión actual: {sys.version}")
        return False
    
    # Verificar paquetes críticos
    critical_packages = ['PyQt5', 'sqlalchemy']
    
    for package in critical_packages:
        try:
            # Manejar el caso especial de PyQt5 en Windows
            if package == 'PyQt5':
                from PyQt5.QtWidgets import QApplication
                debug_print(f"✅ Paquete {package} disponible")
            else:
                __import__(package.lower().replace('-', '_'))
                debug_print(f"✅ Paquete {package} disponible")
        except ImportError as e:
            print(f"❌ Error: Falta paquete {package}. Ejecutar: pip install {package}")
            print(f"   Detalle: {e}")
            return False
    
    return True

# Verificar entorno antes de continuar
if not verify_environment():
    print("\n💡 Sugerencias:")
    print("1. pip install -r requirements.txt")
    print("2. python diagnose_windows.py  # Para diagnóstico completo")
    sys.exit(1)

# Ahora importar módulos de PyQt5 y la aplicación
try:
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt, QCoreApplication
    debug_print("✅ PyQt5 importado correctamente")
except ImportError as e:
    print(f"❌ Error al importar PyQt5: {e}")
    print("\n💡 Soluciones:")
    print("1. pip uninstall PyQt5 && pip install PyQt5==5.15.9")
    print("2. Instalar Visual C++ Redistributable 2015-2019")
    sys.exit(1)

try:
    from controllers.app_controller import AppController
    from utils.database import init_database
    debug_print("✅ Módulos de la aplicación importados correctamente")
except ImportError as e:
    print(f"❌ Error al importar módulos de la aplicación: {e}")
    import traceback
    if DEBUG_MODE:
        traceback.print_exc()
    sys.exit(1)

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
    try:
        QApplication.quit()
    except:
        pass
    sys.exit(0)

def test_qt_application():
    """Probar creación de aplicación Qt básica"""
    debug_print("Probando creación de QApplication...")
    
    try:
        # Verificar si ya existe una aplicación
        existing_app = QApplication.instance()
        if existing_app:
            debug_print("Ya existe una instancia de QApplication")
            return existing_app
        
        # Configuraciones para alta resolución (específico para Windows)
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        if platform.system() == "Windows":
            QCoreApplication.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)
        
        # Crear aplicación PyQt5
        app = QApplication(sys.argv)
        app.setApplicationName("POS RestauranteFast")
        app.setApplicationVersion("2.0")
        
        # Intentar establecer estilo
        try:
            app.setStyle('Fusion')
            debug_print("✅ Estilo Fusion aplicado")
        except:
            debug_print("⚠️  No se pudo aplicar estilo Fusion, usando por defecto")
        
        debug_print("✅ QApplication creada exitosamente")
        return app
        
    except Exception as e:
        print(f"❌ Error al crear QApplication: {e}")
        if DEBUG_MODE:
            import traceback
            traceback.print_exc()
        return None

def main():
    """Función principal del sistema POS"""
    
    # Configurar manejo de señales (solo en sistemas que lo soporten)
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        debug_print("✅ Manejadores de señales configurados")
    except AttributeError:
        debug_print("⚠️  Algunos manejadores de señales no disponibles en este sistema")
    
    print(f"{Colors.CYAN}🚀 Iniciando Sistema POS RestauranteFast...{Colors.RESET}")
    
    if DEBUG_MODE:
        print(f"🐛 MODO DEBUG ACTIVADO")
        print(f"   Python: {sys.version}")
        print(f"   Plataforma: {platform.platform()}")
        print(f"   Directorio: {project_root}")
    
    try:
        # Inicializar base de datos
        print(f"{Colors.BLUE}📂 Inicializando base de datos...{Colors.RESET}")
        init_database()
        print(f"{Colors.GREEN}✅ Base de datos lista{Colors.RESET}")
        
        # Si modo no-gui, salir aquí
        if args.no_gui:
            print("✅ Test sin GUI completado exitosamente")
            return 0
        
        # Probar creación de aplicación Qt
        app = test_qt_application()
        if not app:
            print("❌ No se pudo crear la aplicación Qt")
            return 1
        
        # Configurar aplicación para manejar Ctrl+C
        app.setQuitOnLastWindowClosed(True)
        
        print(f"{Colors.BLUE}🔐 Iniciando sistema de autenticación...{Colors.RESET}")
        
        # Crear controlador principal de la aplicación
        try:
            app_controller = AppController()
            debug_print("✅ AppController creado")
            
            # Asegurar que el controlador no se destruya
            app.app_controller = app_controller
            
            # Iniciar aplicación con login
            app_controller.start_application()
            debug_print("✅ Aplicación iniciada")
            
        except Exception as e:
            print(f"❌ Error al crear AppController: {e}")
            if DEBUG_MODE:
                import traceback
                traceback.print_exc()
            return 1
        
        print(f"{Colors.GREEN}✅ Sistema POS listo para usar!{Colors.RESET}")
        print(f"{Colors.CYAN}💡 Para salir use Ctrl+C o cierre la ventana{Colors.RESET}")
        
        if DEBUG_MODE:
            print(f"🐛 Entrando en bucle principal de la aplicación...")
        
        # Ejecutar aplicación
        return app.exec_()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🚨 Interrupción por teclado detectada{Colors.RESET}")
        return 0
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error crítico en main: {e}{Colors.RESET}")
        
        if DEBUG_MODE:
            import traceback
            traceback.print_exc()
        
        # Mostrar error al usuario si es posible
        try:
            app = QApplication.instance()
            if app:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error Crítico")
                msg.setText(f"Error en el sistema: {str(e)}")
                if DEBUG_MODE:
                    import traceback
                    msg.setDetailedText(traceback.format_exc())
                msg.exec_()
        except:
            pass  # Si no se puede mostrar el diálogo, continuar
            
        return 1
    
    finally:
        print(f"{Colors.CYAN}🔄 Limpiando recursos...{Colors.RESET}")
        try:
            app = QApplication.instance()
            if app:
                app.quit()
        except:
            pass
        print(f"{Colors.GREEN}✅ Sistema POS cerrado correctamente{Colors.RESET}")

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
