"""
Script para probar el filtro de órdenes pagadas en kitchen_orders_window
"""
from controllers.order_controller import OrderController
from models.order import OrderStatus

def test_kitchen_orders_filter():
    """Probar el filtro de órdenes en kitchen orders"""
    controller = OrderController()
    
    print("🧪 Probando filtros de kitchen orders...")
    
    # 1. Obtener todas las órdenes para cocina
    all_orders = controller.get_all_orders_for_kitchen()
    print(f"\n📊 Total órdenes para cocina: {len(all_orders)}")
    
    # 2. Filtrar por cada estado
    for status in [OrderStatus.PENDING, OrderStatus.PREPARING, OrderStatus.READY, 
                   OrderStatus.DELIVERED, OrderStatus.PAID]:
        filtered = [order for order in all_orders if order.status == status.value]
        print(f"   {status.name}: {len(filtered)} órdenes")
        
        # Mostrar algunas órdenes de ejemplo para PAID
        if status == OrderStatus.PAID and filtered:
            print(f"      Ejemplos de órdenes pagadas:")
            for order in filtered[:3]:
                print(f"      - Orden #{order.id}: ${order.total:.2f} - Estado: '{order.status}'")
    
    # 3. Probar específicamente órdenes pagadas
    paid_orders = [order for order in all_orders if order.status == OrderStatus.PAID.value]
    print(f"\n💰 Órdenes pagadas encontradas: {len(paid_orders)}")
    
    if paid_orders:
        print("   Primeras 5 órdenes pagadas:")
        for order in paid_orders[:5]:
            print(f"   - Orden #{order.id}: ${order.total:.2f} - Cliente: {order.customer_name} - Fecha: {order.created_at.strftime('%d/%m/%Y %H:%M')}")
    else:
        print("   ❌ No se encontraron órdenes pagadas")
    
    print("\n✅ Prueba completada!")

if __name__ == "__main__":
    test_kitchen_orders_filter()
