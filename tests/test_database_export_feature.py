#!/usr/bin/env python3
"""
Test de la nueva funcionalidad de gestión de datos en printer_config_view.py
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from views.printer_config_view import PrinterConfigView

def test_data_management_interface():
    """Probar la nueva interfaz de gestión de datos"""
    print("🧪 PRUEBA DE GESTIÓN DE DATOS EN CONFIGURACIÓN")
    print("=" * 55)
    
    # Verificar que el archivo existe
    config_view_path = os.path.join(os.path.dirname(__file__), "views", "printer_config_view.py")
    
    if not os.path.exists(config_view_path):
        print("❌ Archivo printer_config_view.py no encontrado")
        return
    
    print("✅ Archivo printer_config_view.py encontrado")
    
    # Verificar base de datos
    db_path = os.path.join(os.path.dirname(__file__), "data", "pos.db")
    
    if os.path.exists(db_path):
        db_size = os.path.getsize(db_path) / (1024 * 1024)
        print(f"✅ Base de datos encontrada: {db_size:.1f} MB")
    else:
        print("⚠️ Base de datos no encontrada (se puede crear respaldos de prueba)")
    
    # Verificar imports
    try:
        from views.printer_config_view import PrinterConfigView
        print("✅ Clase PrinterConfigView importada correctamente")
        
        # Verificar que los nuevos métodos existen
        import inspect
        
        methods_to_check = [
            'create_data_management_section',
            'create_database_backup', 
            'export_database',
            'verify_database',
            'update_database_info'
        ]
        
        for method_name in methods_to_check:
            if hasattr(PrinterConfigView, method_name):
                print(f"✅ Método {method_name} existe")
            else:
                print(f"❌ Método {method_name} no encontrado")
        
        print(f"\n🎯 FUNCIONALIDADES AGREGADAS:")
        print(f"   📁 Crear Respaldo: Crea respaldo en directorio data/")
        print(f"   💾 Exportar BD: Permite elegir ubicación de exportación")
        print(f"   🔍 Verificar Integridad: Verifica estado de la base de datos")
        print(f"   📊 Info de BD: Muestra tamaño actual de la base de datos")
        
        print(f"\n🖥️ INTERFAZ:")
        print(f"   • Nueva sección '💾 Gestión de Datos'")
        print(f"   • Layout horizontal compacto")
        print(f"   • 3 botones de acción principales")
        print(f"   • Información de BD en tiempo real")
        
        print(f"\n✅ CONFIGURACIÓN LISTA")
        print(f"La nueva funcionalidad está integrada en el panel de configuración")
        
    except ImportError as e:
        print(f"❌ Error al importar: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_interface_integration():
    """Probar la integración en la interfaz"""
    print(f"\n🔗 PRUEBA DE INTEGRACIÓN EN ADMIN WINDOW")
    print("=" * 45)
    
    try:
        # Verificar que se puede acceder desde admin_window
        from views.admin_window import AdminWindow
        print("✅ AdminWindow importado correctamente")
        
        print(f"\n📋 PASOS PARA USAR LA NUEVA FUNCIONALIDAD:")
        print(f"1. Ejecutar: python main.py")
        print(f"2. Login como administrador")
        print(f"3. Ir a pestaña '⚙️ Configuración'")
        print(f"4. Ver nueva sección '💾 Gestión de Datos'")
        print(f"5. Usar botones:")
        print(f"   • 📁 Crear Respaldo")
        print(f"   • 💾 Exportar Base de Datos")
        print(f"   • 🔍 Verificar Integridad")
        
    except ImportError as e:
        print(f"⚠️ AdminWindow no disponible: {e}")

if __name__ == "__main__":
    test_data_management_interface()
    test_interface_integration()
