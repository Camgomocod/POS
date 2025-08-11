#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad mejorada 
de selección de texto en los formularios de productos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from views.menu_management_window import ProductFormDialog
from models.product import Product
from models.category import Category

def test_product_form():
    """Probar el formulario de productos con la nueva funcionalidad"""
    app = QApplication(sys.argv)
    
    print("🧪 Probando formulario de productos...")
    print("✨ Nuevas funcionalidades:")
    print("  - Click en campos de precio/costo/stock/tiempo: selecciona todo el texto")
    print("  - Click en campo de nombre: selecciona todo el texto") 
    print("  - Valores iniciales más intuitivos")
    print()
    print("📝 Instrucciones de prueba:")
    print("  1. Haz click en cualquier campo numérico")
    print("  2. Verifica que se selecciona todo el contenido")
    print("  3. Escribe directamente para reemplazar el valor")
    print("  4. La experiencia debe ser más fluida y rápida")
    print()
    
    # Crear diálogo de nuevo producto
    dialog = ProductFormDialog(None, is_edit=False)
    dialog.setWindowTitle("🧪 Prueba: Nuevo Producto - Funcionalidad Mejorada")
    
    # Mostrar el diálogo
    result = dialog.exec_()
    
    if result:
        print("✅ Producto creado exitosamente")
    else:
        print("❌ Operación cancelada")
    
    app.quit()

if __name__ == "__main__":
    test_product_form()
