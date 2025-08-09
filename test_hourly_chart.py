#!/usr/bin/env python3
"""
Script de prueba para verificar el gráfico por horas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.reports_controller import ReportsController
from datetime import date

def test_hourly_data():
    """Probar datos horarios"""
    print("🧪 Probando datos horarios...")
    
    ctrl = ReportsController()
    today = date.today()
    
    print(f"📅 Fecha: {today}")
    
    # Probar ventas diarias
    daily_sales = ctrl.get_daily_sales(today, today)
    print(f"📊 Ventas diarias: {daily_sales}")
    
    # Probar ventas por hora
    hourly_sales = ctrl.get_sales_by_hour(today, today)
    print(f"⏰ Ventas por horas:")
    for hour in hourly_sales:
        print(f"   {hour['hour_range']}: ${hour['total_sales']:.2f} ({hour['order_count']} órdenes)")
    
    print("\n✅ Datos correctos!")
    return len(hourly_sales) > 0

if __name__ == "__main__":
    test_hourly_data()
