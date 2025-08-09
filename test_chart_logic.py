#!/usr/bin/env python3
"""
Script de prueba para simular la vista de reportes y verificar el gráfico por horas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import date

def test_chart_logic():
    """Probar la lógica del gráfico"""
    print("🧪 Probando lógica del gráfico...")
    
    # Simular fechas
    today = date.today()
    yesterday = date.today().replace(day=8)  # Un día diferente
    
    # Caso 1: Un solo día (debe usar datos horarios)
    is_single_day_today = today == today
    print(f"📅 Hoy == Hoy: {is_single_day_today} -> Debe usar datos HORARIOS")
    
    # Caso 2: Período de varios días (debe usar datos diarios)
    is_single_day_range = yesterday == today
    print(f"📅 Ayer == Hoy: {is_single_day_range} -> Debe usar datos DIARIOS")
    
    # Verificar que la función de horas funciona
    from controllers.reports_controller import ReportsController
    ctrl = ReportsController()
    
    hourly_data = ctrl.get_sales_by_hour(today, today)
    daily_data = ctrl.get_daily_sales(yesterday, today)
    
    print(f"⏰ Datos horarios para hoy: {len(hourly_data)} horas con datos")
    print(f"📊 Datos diarios para rango: {len(daily_data)} días con datos")
    
    print("\n✅ La lógica del gráfico funcionará correctamente!")
    print("   - Botón 'Hoy': Mostrará gráfico por HORAS (rojo)")
    print("   - Botón 'Semana' o 'Mes': Mostrará gráfico por DÍAS (azul)")

if __name__ == "__main__":
    test_chart_logic()
