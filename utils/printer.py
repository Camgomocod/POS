# utils/printer.py
import os
import tempfile
import subprocess
import platform
from datetime import datetime

class ReceiptPrinter:
    def __init__(self):
        self.restaurant_name = "FAST FOOD RESTAURANT"
        self.restaurant_address = "Calle Principal #123"
        self.restaurant_phone = "Tel: (123) 456-7890"
    
    def print_receipt(self, order, cart_items):
        """Generar e imprimir recibo"""
        receipt_content = self.generate_receipt_content(order, cart_items)
        
        # Guardar en archivo temporal
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_file.write(receipt_content)
        temp_file.close()
        
        # Abrir con el programa predeterminado (para imprimir) sin usar terminal
        try:
            self._open_file(temp_file.name)
        except Exception as e:
            print(f"Error al abrir recibo: {e}")
        
        return temp_file.name
    
    def _open_file(self, filepath):
        """Abrir archivo de forma segura según el SO"""
        system = platform.system()
        
        if system == "Windows":
            os.startfile(filepath)
        elif system == "Darwin":  # macOS
            subprocess.run(['open', filepath], check=False)
        else:  # Linux
            # Usar subprocess sin shell para evitar problemas de terminal
            subprocess.run(['xdg-open', filepath], check=False, 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def generate_receipt_content(self, order, cart_items):
        """Generar contenido del recibo"""
        content = []
        
        # Encabezado
        content.append("=" * 40)
        content.append(f"{self.restaurant_name:^40}")
        content.append(f"{self.restaurant_address:^40}")
        content.append(f"{self.restaurant_phone:^40}")
        content.append("=" * 40)
        content.append("")
        
        # Información de la orden
        content.append(f"Orden #: {order.id}")
        content.append(f"Fecha: {order.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        content.append("")
        content.append("-" * 40)
        content.append("PRODUCTOS")
        content.append("-" * 40)
        
        # Items
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            subtotal = product.price * quantity
            
            content.append(f"{product.name}")
            content.append(f"  {quantity} x ${product.price:.2f} = ${subtotal:.2f}")
            content.append("")
        
        # Total
        content.append("-" * 40)
        content.append(f"{'TOTAL:':>30} ${order.total:.2f}")
        content.append("=" * 40)
        content.append("")
        content.append("¡Gracias por su compra!")
        content.append("Vuelva pronto")
        content.append("")
        
        return "\n".join(content)
    
    def print_order_ticket(self, order, cart_items):
        """Generar e imprimir ticket de orden (sin pago)"""
        ticket_content = self.generate_order_ticket_content(order, cart_items)
        
        # Guardar en archivo temporal
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_file.write(ticket_content)
        temp_file.close()
        
        # Abrir con el programa predeterminado
        try:
            self._open_file(temp_file.name)
        except Exception as e:
            print(f"Error al abrir ticket: {e}")
        
        return temp_file.name
    
    def generate_order_ticket_content(self, order, cart_items):
        """Generar contenido del ticket de orden"""
        content = []
        
        # Encabezado
        content.append("=" * 40)
        content.append(f"{self.restaurant_name:^40}")
        content.append(f"{self.restaurant_address:^40}")
        content.append(f"{self.restaurant_phone:^40}")
        content.append("=" * 40)
        content.append("")
        content.append("TICKET DE ORDEN")
        content.append(f"Orden #: {order.id}")
        content.append(f"Cliente: {order.customer_name}")
        if order.table_number:
            content.append(f"Mesa: {order.table_number}")
        else:
            content.append("Para llevar")
        content.append(f"Fecha: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        content.append("-" * 40)
        content.append("ITEMS PEDIDOS:")
        content.append("-" * 40)
        
        # Items
        for item_data in cart_items:
            product = item_data['product']
            quantity = item_data['quantity']
            subtotal = product.price * quantity
            content.append(f"{product.name}")
            content.append(f"  {quantity} x ${product.price:.2f} = ${subtotal:.2f}")
            content.append("")
        
        # Total
        content.append("-" * 40)
        content.append(f"{'TOTAL A PAGAR:':>30} ${order.total:.2f}")
        content.append("=" * 40)
        content.append("")
        content.append("ESTADO: PENDIENTE DE PREPARAR")
        content.append("El pago se realizará al final del servicio")
        content.append("")
        content.append("¡Gracias por su pedido!")
        content.append("")
        
        return "\n".join(content)
