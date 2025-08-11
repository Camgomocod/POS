#!/usr/bin/env python3
"""
Test para identificar qué importación específica en AdminWindow causa el cuelgue
"""

import sys
import os
import traceback

# Configurar entorno
os.environ['QT_QPA_PLATFORM'] = 'windows'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

# Agregar directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

print("🔍 TEST DE IMPORTACIONES DE AdminWindow")
print("=" * 42)

try:
    # PyQt5 básico
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    print("✅ PyQt5 básico OK")

    # Probar cada importación de AdminWindow una por una
    print("\n📋 Probando importaciones de AdminWindow:")

    print("   1. PyQt5 widgets...")
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QFrame, QStackedWidget, QApplication, QMessageBox,
        QTabWidget, QScrollArea, QGridLayout, QSizePolicy,
        QTableWidget, QTableWidgetItem, QAbstractItemView
    )
    print("   ✅ PyQt5 widgets OK")

    print("   2. PyQt5 core...")
    from PyQt5.QtCore import Qt, pyqtSignal, QTimer
    print("   ✅ PyQt5 core OK")

    print("   3. PyQt5 gui...")
    from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QPen, QColor
    print("   ✅ PyQt5 gui OK")

    print("   4. utils.colors...")
    from utils.colors import ColorPalette, CommonStyles
    print("   ✅ utils.colors OK")

    print("   5. controllers.auth_controller...")
    from controllers.auth_controller import AuthController
    print("   ✅ auth_controller OK")

    print("   6. views.user_management_window...")
    try:
        from views.user_management_window import UserManagementWidget
        print("   ✅ user_management_window OK")
    except Exception as e:
        print(f"   ❌ ERROR en user_management_window: {e}")
        traceback.print_exc()

    print("   7. views.menu_management_window...")
    try:
        from views.menu_management_window import MenuManagementWidget
        print("   ✅ menu_management_window OK")
    except Exception as e:
        print(f"   ❌ ERROR en menu_management_window: {e}")
        traceback.print_exc()

    print("   8. views.reports_view...")
    try:
        from views.reports_view import ReportsView
        print("   ✅ reports_view OK")
    except Exception as e:
        print(f"   ❌ ERROR en reports_view: {e}")
        traceback.print_exc()

    print("   9. views.printer_config_view...")
    try:
        from views.printer_config_view import PrinterConfigView
        print("   ✅ printer_config_view OK")
    except Exception as e:
        print(f"   ❌ ERROR en printer_config_view: {e}")
        traceback.print_exc()

    print("   10. datetime...")
    from datetime import datetime, timedelta
    print("   ✅ datetime OK")

    print("   11. sys y time...")
    import sys
    import time
    print("   ✅ sys y time OK")

    # Ahora intentar importar AdminWindow completo
    print("\n🎯 Importando AdminWindow completo...")
    from views.admin_window import AdminWindow
    print("✅ AdminWindow importado exitosamente!")

    # Probar crear una instancia
    print("\n🧪 Probando crear instancia de AdminWindow...")
    try:
        # Crear un usuario dummy para el test
        from models.user import User, UserRole
        dummy_user = User()
        dummy_user.username = "test"
        dummy_user.role = UserRole.ADMIN
        
        admin_window = AdminWindow(dummy_user)
        print("✅ AdminWindow creado exitosamente!")
        
        admin_window.deleteLater()
        
    except Exception as e:
        print(f"❌ Error creando AdminWindow: {e}")
        traceback.print_exc()

    print("\n🎉 TODAS LAS IMPORTACIONES FUNCIONAN!")

except Exception as e:
    print(f"\n❌ ERROR EN IMPORTACIÓN: {e}")
    traceback.print_exc()

finally:
    print("\n" + "="*50)
    print("Si todas las importaciones pasaron, el problema puede estar")
    print("en una dependencia circular o en el momento de ejecución")
    print("="*50)

input("\nPresiona Enter para salir...")
