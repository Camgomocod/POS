#!/usr/bin/env python3
# verify_thermal_printer_integration.py
"""
Script de verificación de la integración de impresoras térmicas
No requiere librerías específicas de impresión
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_module_imports():
    """Verificar que los módulos se importan correctamente"""
    print("🔍 Verificando importaciones de módulos...")
    
    try:
        from utils.printer import ThermalPrinter, ReceiptPrinter
        print("✅ utils.printer - ThermalPrinter y ReceiptPrinter importados")
    except Exception as e:
        print(f"❌ Error al importar utils.printer: {e}")
        return False
    
    try:
        from views.printer_config_view import PrinterConfigView
        print("✅ views.printer_config_view - PrinterConfigView importado")
    except Exception as e:
        print(f"❌ Error al importar printer_config_view: {e}")
        return False
    
    try:
        from views.admin_window import AdminWindow
        print("✅ views.admin_window - AdminWindow importado (con integración de printer)")
    except Exception as e:
        print(f"❌ Error al importar admin_window: {e}")
        return False
    
    try:
        from views.kitchen_orders_window import KitchenOrdersWindow
        print("✅ views.kitchen_orders_window - KitchenOrdersWindow importado (con thermal printer)")
    except Exception as e:
        print(f"❌ Error al importar kitchen_orders_window: {e}")
        return False
    
    return True

def verify_thermal_printer_functionality():
    """Verificar funcionalidad básica de ThermalPrinter"""
    print("\n🛠️ Verificando funcionalidad básica...")
    
    from utils.printer import ThermalPrinter
    
    # Crear instancia
    printer = ThermalPrinter()
    print("✅ Instancia de ThermalPrinter creada")
    
    # Verificar métodos básicos
    try:
        configured = printer.is_configured()
        print(f"✅ is_configured() funciona: {configured}")
    except Exception as e:
        print(f"❌ Error en is_configured(): {e}")
        return False
    
    # Verificar detección (sin requerir librerías específicas)
    try:
        printers = ThermalPrinter.get_available_printers()
        print(f"✅ get_available_printers() funciona: {len(printers)} impresoras encontradas")
        
        # Si no hay impresoras, es normal en entorno sin hardware
        if len(printers) == 0:
            print("💡 No se detectaron impresoras (normal sin hardware térmico)")
        else:
            for i, p in enumerate(printers):
                print(f"   {i+1}. {p.get('name', 'Unknown')} ({p.get('type', 'unknown')})")
    except Exception as e:
        print(f"❌ Error en get_available_printers(): {e}")
        return False
    
    # Verificar generación de ESC/POS (sin imprimir)
    try:
        test_data = printer._generate_test_page_57mm()
        print(f"✅ Generación de datos ESC/POS funciona: {len(test_data)} bytes")
    except Exception as e:
        print(f"❌ Error generando datos ESC/POS: {e}")
        return False
    
    return True

def verify_integration_files():
    """Verificar que los archivos de integración están correctos"""
    print("\n📁 Verificando archivos de integración...")
    
    # Verificar archivos principales
    files_to_check = [
        "/home/llamqak/Projects/POS/utils/printer.py",
        "/home/llamqak/Projects/POS/views/printer_config_view.py",
        "/home/llamqak/Projects/POS/views/admin_window.py",
        "/home/llamqak/Projects/POS/views/kitchen_orders_window.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {os.path.basename(file_path)} existe")
        else:
            print(f"❌ {os.path.basename(file_path)} no encontrado")
            return False
    
    # Verificar integración en admin_window.py
    try:
        with open("/home/llamqak/Projects/POS/views/admin_window.py", 'r') as f:
            content = f.read()
            if "from views.printer_config_view import PrinterConfigView" in content:
                print("✅ admin_window.py importa PrinterConfigView")
            else:
                print("❌ admin_window.py no importa PrinterConfigView")
                return False
                
            if "PrinterConfigView()" in content:
                print("✅ admin_window.py instancia PrinterConfigView")
            else:
                print("❌ admin_window.py no instancia PrinterConfigView")
                return False
    except Exception as e:
        print(f"❌ Error verificando admin_window.py: {e}")
        return False
    
    # Verificar integración en kitchen_orders_window.py
    try:
        with open("/home/llamqak/Projects/POS/views/kitchen_orders_window.py", 'r') as f:
            content = f.read()
            if "from utils.printer import ThermalPrinter" in content:
                print("✅ kitchen_orders_window.py importa ThermalPrinter")
            else:
                print("❌ kitchen_orders_window.py no importa ThermalPrinter")
                return False
                
            if "printer.print_receipt" in content:
                print("✅ kitchen_orders_window.py llama print_receipt")
            else:
                print("❌ kitchen_orders_window.py no llama print_receipt")
                return False
    except Exception as e:
        print(f"❌ Error verificando kitchen_orders_window.py: {e}")
        return False
    
    return True

def verify_database_compatibility():
    """Verificar compatibilidad con base de datos"""
    print("\n🗄️ Verificando compatibilidad con base de datos...")
    
    try:
        from controllers.order_controller import OrderController
        from models.order import OrderStatus
        
        order_ctrl = OrderController()
        
        # Verificar que puede obtener órdenes pagadas
        paid_orders = order_ctrl.get_orders_by_status(OrderStatus.PAID.value)
        print(f"✅ Órdenes pagadas disponibles: {len(paid_orders)}")
        
        if len(paid_orders) > 0:
            # Verificar que puede obtener detalles de orden
            test_order = paid_orders[0]
            order_details = order_ctrl.get_order_details(test_order.id)
            
            if order_details and hasattr(order_details, 'items'):
                print(f"✅ Detalles de orden funcionan: orden #{order_details.id} con {len(order_details.items)} items")
            else:
                print("❌ No se pudieron obtener detalles de orden")
                return False
        else:
            print("💡 No hay órdenes pagadas (cree algunas para probar impresión)")
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False
    
    return True

def main():
    """Función principal de verificación"""
    print("=" * 70)
    print("🔧 VERIFICACIÓN DE INTEGRACIÓN DE IMPRESORAS TÉRMICAS")
    print("=" * 70)
    print()
    
    all_checks_passed = True
    
    # Verificaciones
    checks = [
        ("Importaciones de módulos", verify_module_imports),
        ("Funcionalidad de ThermalPrinter", verify_thermal_printer_functionality),
        ("Archivos de integración", verify_integration_files),
        ("Compatibilidad con base de datos", verify_database_compatibility)
    ]
    
    for check_name, check_function in checks:
        print(f"🧪 {check_name}...")
        print("-" * 50)
        
        try:
            result = check_function()
            if result:
                print(f"✅ {check_name}: PASSED")
            else:
                print(f"❌ {check_name}: FAILED")
                all_checks_passed = False
        except Exception as e:
            print(f"❌ {check_name}: ERROR - {e}")
            all_checks_passed = False
        
        print()
    
    # Resumen final
    print("=" * 70)
    if all_checks_passed:
        print("🎉 TODAS LAS VERIFICACIONES PASARON")
        print("✅ El sistema de impresoras térmicas está correctamente integrado")
        print()
        print("📋 PRÓXIMOS PASOS:")
        print("1. Conecte una impresora térmica USB de 57mm")
        print("2. Abra el panel de administración")
        print("3. Vaya a '⚙️ Configuración' para detectar y configurar la impresora")
        print("4. Procese un pago en 'Órdenes de Cocina' para probar impresión automática")
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("💡 Revise los errores arriba y corrija los problemas encontrados")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
