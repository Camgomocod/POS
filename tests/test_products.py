#!/usr/bin/env python3

from controllers.reports_controller import ReportsController
from datetime import datetime, timedelta

def test_products_report():
    """Probar el reporte de productos"""
    print('🧪 Probando reporte de productos...')
    
    # Crear controlador
    reports_ctrl = ReportsController()
    
    # Últimos 30 días
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    print(f'📅 Rango: {start_date} a {end_date}')
    
    # Obtener productos
    products = reports_ctrl.get_detailed_products_report(start_date, end_date)
    print(f'📊 Productos encontrados: {len(products)}')
    
    if products:
        print('\n🏆 Top 10 productos:')
        for i, p in enumerate(products[:10], 1):
            name = p["name"]
            quantity = p["total_quantity"]
            revenue = p["total_revenue"]
            category = p.get("category", "N/A")
            print(f'{i:2}. {name:<25} | Cant: {quantity:3} | ${revenue:>8,.0f} | {category}')
    else:
        print('❌ No se encontraron productos')
    
    return products

if __name__ == "__main__":
    test_products_report()
