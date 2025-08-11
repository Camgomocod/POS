#!/usr/bin/env python3

from controllers.reports_controller import ReportsController
from datetime import datetime, timedelta
import csv

def test_csv_export():
    """Probar la exportación de CSV mejorada"""
    print('🧪 Probando exportación CSV mejorada...')
    
    # Crear controlador
    reports_ctrl = ReportsController()
    
    # Últimos 30 días
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    print(f'📅 Rango: {start_date} a {end_date}')
    
    # Obtener datos
    sales_summary = reports_ctrl.get_sales_summary(start_date, end_date)
    products_data = reports_ctrl.get_detailed_products_report(start_date, end_date)
    monthly_data = reports_ctrl.get_daily_sales(start_date, end_date)
    
    print(f'📊 Resumen de ventas: {sales_summary}')
    print(f'📊 Productos encontrados: {len(products_data)}')
    print(f'📊 Datos diarios: {len(monthly_data) if monthly_data else 0}')
    
    # Crear archivo de prueba
    file_path = '/home/llamqak/Projects/POS/test_export.csv'
    
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Encabezado del reporte
        writer.writerow(['REPORTE COMPLETO DE VENTAS - PRUEBA'])
        writer.writerow([f'Período: {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}'])
        writer.writerow([f'Fecha de generación: {datetime.now().strftime("%d/%m/%Y %H:%M")}'])
        writer.writerow([])
        
        # Resumen general
        writer.writerow(['RESUMEN EJECUTIVO'])
        if sales_summary:
            total_sales = sales_summary.get('total_sales', 0)
            total_orders = sales_summary.get('total_orders', 0)
            avg_ticket = sales_summary.get('avg_ticket', 0)
            
            writer.writerow(['Total Ventas', f"${total_sales:,.0f} COP"])
            writer.writerow(['Total Órdenes', total_orders])
            writer.writerow(['Ticket Promedio', f"${avg_ticket:,.0f} COP"])
            
            # Calcular días del período para promedio diario
            days = (end_date - start_date).days + 1
            avg_daily_sales = total_sales / days if days > 0 else 0
            avg_daily_orders = total_orders / days if days > 0 else 0
            
            writer.writerow(['Promedio Ventas Diarias', f"${avg_daily_sales:,.0f} COP"])
            writer.writerow(['Promedio Órdenes Diarias', f"{avg_daily_orders:.1f}"])
        writer.writerow([])
        
        # Top 5 productos más vendidos
        writer.writerow(['TOP 5 PRODUCTOS MÁS VENDIDOS'])
        writer.writerow(['Posición', 'Producto', 'Cantidad Vendida', 'Ingresos (COP)', '% del Total', 'Categoría'])
        
        if products_data:
            total_revenue = sum(p.get('total_revenue', 0.0) for p in products_data)
            top_5_products = products_data[:5]
            
            for i, product in enumerate(top_5_products, 1):
                name = product.get('name', 'N/A')
                quantity = product.get('total_quantity', 0)
                revenue = product.get('total_revenue', 0.0)
                percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                category = product.get('category', 'N/A')
                
                writer.writerow([
                    f"#{i}", 
                    name, 
                    quantity, 
                    f"{revenue:,.0f}", 
                    f"{percentage:.1f}%",
                    category
                ])
    
    print(f'✅ Archivo CSV creado exitosamente: {file_path}')
    
    # Mostrar primeras líneas del archivo
    print('\n📄 Primeras líneas del archivo:')
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if i > 15:  # Mostrar solo las primeras 15 líneas
                break
            print(f'{i:2}: {line.strip()}')

if __name__ == "__main__":
    test_csv_export()
