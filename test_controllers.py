#!/usr/bin/env python3
"""
Script para probar los controladores corregidos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.payment_controller import PaymentController
from controllers.order_controller import OrderController
from models.order import OrderStatus

def test_controllers():
    print("🧪 Probando controladores...")
    
    # Test PaymentController
    print("\n1. PaymentController:")
    pc = PaymentController()
    result = pc.get_payment_history(page=1, page_size=5)
    print(f"   📊 Total órdenes pagadas: {result['total_count']}")
    for order in result['orders'][:3]:
        print(f"   🍽️ Orden #{order.id} (Mesa {order.table_number or 'N/A'}): ${order.total:.2f} - Estado: {order.status}")
    
    # Test OrderController
    print("\n2. OrderController:")
    oc = OrderController()
    
    # Órdenes activas
    active_orders = oc.get_active_orders()
    print(f"   📋 Órdenes activas: {len(active_orders)}")
    
    # Todas las órdenes para cocina
    kitchen_orders = oc.get_all_orders_for_kitchen()
    print(f"   🍳 Órdenes para cocina: {len(kitchen_orders)}")
    
    # Contar por estado
    states = {}
    for order in kitchen_orders:
        state = order.status
        states[state] = states.get(state, 0) + 1
    
    print("   📈 Órdenes por estado:")
    for state, count in states.items():
        print(f"      {state}: {count}")
    
    print("\n✅ Controladores funcionando correctamente!")

if __name__ == "__main__":
    test_controllers()
