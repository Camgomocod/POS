# utils/printer.py
import os
import tempfile
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
        
        # Abrir con el programa predeterminado (para imprimir)
        try:
            os.startfile(temp_file.name)  # Windows
        except AttributeError:
            try:
                os.system(f'open {temp_file.name}')  # macOS
            except:
                os.system(f'xdg-open {temp_file.name}')  # Linux
        
        return temp_file.name
    
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
