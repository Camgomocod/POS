"""
Script para actualizar los valores de status en la base de datos para que coincidan con los enum
"""
import sqlite3
from models.order import OrderStatus

# Mapeo de los valores actuales a los valores del enum
status_mapping = {
    'paid': OrderStatus.PAID.value,
    'pending': OrderStatus.PENDING.value,
    'preparing': OrderStatus.PREPARING.value,
    'ready': OrderStatus.READY.value,
    'delivered': OrderStatus.DELIVERED.value,
    'cancelled': OrderStatus.CANCELLED.value
}

def update_database():
    conn = sqlite3.connect('data/pos.db')
    cursor = conn.cursor()
    
    # Verificar valores actuales
    cursor.execute("SELECT DISTINCT status FROM orders")
    current_statuses = [row[0] for row in cursor.fetchall()]
    print(f"Estados actuales en la BD: {current_statuses}")
    
    # Contar órdenes por estado
    cursor.execute("SELECT status, COUNT(*) FROM orders GROUP BY status")
    status_counts = cursor.fetchall()
    print("\nConteo por estado:")
    for status, count in status_counts:
        print(f"  {status}: {count} órdenes")
    
    # Actualizar cada estado
    for old_status, new_status in status_mapping.items():
        cursor.execute("UPDATE orders SET status = ? WHERE status = ?", (new_status, old_status))
        updated = cursor.rowcount
        if updated > 0:
            print(f"Actualizado {updated} órdenes de '{old_status}' a '{new_status}'")
    
    # Verificar después de la actualización
    cursor.execute("SELECT DISTINCT status FROM orders")
    new_statuses = [row[0] for row in cursor.fetchall()]
    print(f"\nEstados después de actualización: {new_statuses}")
    
    conn.commit()
    conn.close()
    print("\nBase de datos actualizada exitosamente!")

if __name__ == "__main__":
    update_database()
