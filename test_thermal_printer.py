#!/usr/bin/env python3
# test_thermal_printer.py
"""
Script de prueba para la funcionalidad de impresoras térmicas USB de 57mm
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.printer import ThermalPrinter
from controllers.order_controller import OrderController
from models.order import OrderStatus

def test_printer_detection():
    """Probar detección de impresoras USB"""
    print("🔍 Detectando impresoras USB disponibles...")
    printers = ThermalPrinter.get_available_printers()
    
    if not printers:
        print("❌ No se detectaron impresoras USB.")
        print("💡 Asegúrese de que:")
        print("   - La impresora térmica esté conectada por USB")
        print("   - Los drivers estén instalados")
        print("   - La impresora esté encendida")
        return False
    
    print(f"✅ Se detectaron {len(printers)} impresoras:")
    for i, printer in enumerate(printers, 1):
        print(f"   {i}. {printer['name']}")
        print(f"      Tipo: {printer['type']}")
        print(f"      Conexión: {printer['connection']}")
        print(f"      Estado: {printer['status']}")
        if 'port' in printer:
            print(f"      Puerto: {printer['port']}")
        if 'device_uri' in printer:
            print(f"      URI: {printer['device_uri']}")
        print()
    
    return printers

def test_printer_configuration():
    """Probar configuración de impresora"""
    print("⚙️ Probando configuración de impresora...")
    
    printer = ThermalPrinter()
    
    if printer.is_configured():
        print(f"✅ Impresora configurada: {printer.printer_name}")
        print(f"   Tipo de conexión: {printer.connection_type}")
        print(f"   Ancho de papel: {printer.paper_width} caracteres")
        print(f"   Corte automático: {'Sí' if printer.auto_cut else 'No'}")
        return True
    else:
        print("❌ No hay impresora configurada")
        print("💡 Configure una impresora desde el panel de administración")
        return False

def test_thermal_receipt():
    """Probar impresión de recibo térmico"""
    print("🖨️ Probando impresión de recibo térmico...")
    
    printer = ThermalPrinter()
    
    if not printer.is_configured():
        print("❌ No hay impresora configurada para prueba")
        return False
    
    # Obtener una orden pagada para prueba
    order_ctrl = OrderController()
    paid_orders = order_ctrl.get_orders_by_status(OrderStatus.PAID.value)
    
    if not paid_orders:
        print("❌ No hay órdenes pagadas para probar")
        print("💡 Procese una orden de pago primero")
        return False
    
    # Usar la primera orden pagada
    test_order = paid_orders[0]
    test_order_details = order_ctrl.get_order_details(test_order.id)
    
    if not test_order_details or not test_order_details.items:
        print("❌ No se pudieron obtener detalles de la orden")
        return False
    
    print(f"📄 Imprimiendo recibo de orden #{test_order_details.id}")
    print(f"   Cliente: {test_order_details.customer_name}")
    print(f"   Total: ${test_order_details.total:.2f}")
    print(f"   Items: {len(test_order_details.items)}")
    
    try:
        success = printer.print_receipt(test_order_details, "efectivo")
        
        if success:
            print("✅ Recibo enviado a impresora térmica exitosamente")
            print("💡 Verifique que se haya impreso correctamente")
            return True
        else:
            print("❌ Error al enviar recibo a impresora")
            return False
            
    except Exception as e:
        print(f"❌ Error durante impresión: {e}")
        return False

def test_print_page():
    """Probar página de prueba"""
    print("📝 Probando página de prueba...")
    
    printer = ThermalPrinter()
    
    if not printer.is_configured():
        print("❌ No hay impresora configurada")
        return False
    
    try:
        success = printer.test_print()
        
        if success:
            print("✅ Página de prueba enviada exitosamente")
            print("💡 Verifique que se haya impreso correctamente")
            return True
        else:
            print("❌ Error al enviar página de prueba")
            return False
            
    except Exception as e:
        print(f"❌ Error durante impresión de prueba: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("🔧 PRUEBA DE IMPRESORAS TÉRMICAS USB 57MM")
    print("=" * 60)
    print()
    
    # 1. Detectar impresoras
    printers = test_printer_detection()
    print()
    
    # 2. Verificar configuración
    config_ok = test_printer_configuration()
    print()
    
    # 3. Si hay configuración, probar impresión
    if config_ok:
        print("🧪 INICIANDO PRUEBAS DE IMPRESIÓN")
        print("-" * 40)
        
        # Página de prueba
        test_print_page()
        print()
        
        # Recibo real
        test_thermal_receipt()
        print()
    
    print("=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")
    
    if not printers:
        print("📋 RESUMEN: No se detectaron impresoras USB")
        print("💡 ACCIÓN: Conecte una impresora térmica USB y vuelva a intentar")
    elif not config_ok:
        print("📋 RESUMEN: Impresoras detectadas pero no configuradas")
        print("💡 ACCIÓN: Configure una impresora desde el panel de administración")
    else:
        print("📋 RESUMEN: Sistema de impresión térmico listo")
        print("💡 ACCIÓN: Las impresiones automáticas funcionarán al procesar pagos")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
