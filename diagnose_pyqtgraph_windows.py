#!/usr/bin/env python3
"""
Script de diagnóstico para PyQtGraph en Windows 11
Diagnóstica problemas específicos con PyQtGraph después de la migración
"""

import sys
import os

print("🔍 DIAGNÓSTICO PYQTGRAPH PARA WINDOWS 11")
print("=" * 50)

# 1. Verificar entorno básico
print("1. Verificando entorno básico...")
print(f"   Python: {sys.version}")
print(f"   Plataforma: {sys.platform}")

# 2. Probar PyQt5 básico
print("\n2. Probando PyQt5 básico...")
try:
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtCore import Qt
    print("   ✅ PyQt5 básico funciona")
except Exception as e:
    print(f"   ❌ Error con PyQt5: {e}")
    sys.exit(1)

# 3. Probar imports individuales
print("\n3. Probando imports PyQtGraph...")
try:
    import pyqtgraph as pg
    print("   ✅ pyqtgraph importado")
except Exception as e:
    print(f"   ❌ Error importando pyqtgraph: {e}")
    sys.exit(1)

try:
    from pyqtgraph import PlotWidget
    print("   ✅ PlotWidget importado")
except Exception as e:
    print(f"   ❌ Error importando PlotWidget: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("   ✅ numpy importado")
except Exception as e:
    print(f"   ❌ Error importando numpy: {e}")

# 4. Probar configuración de PyQtGraph
print("\n4. Probando configuración PyQtGraph...")
try:
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k') 
    pg.setConfigOption('antialias', True)
    print("   ✅ Configuración PyQtGraph aplicada")
except Exception as e:
    print(f"   ❌ Error configurando PyQtGraph: {e}")

# 5. Probar creación de QApplication
print("\n5. Probando QApplication...")
try:
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    print("   ✅ QApplication creada")
except Exception as e:
    print(f"   ❌ Error creando QApplication: {e}")
    sys.exit(1)

# 6. Probar creación de PlotWidget
print("\n6. Probando PlotWidget...")
try:
    plot_widget = PlotWidget(title="Test Plot")
    print("   ✅ PlotWidget creado")
except Exception as e:
    print(f"   ❌ Error creando PlotWidget: {e}")
    print(f"   Detalles: {str(e)}")
    import traceback
    traceback.print_exc()

# 7. Probar imports de reports_view
print("\n7. Probando imports específicos de reports_view...")
try:
    from controllers.reports_controller import ReportsController
    print("   ✅ ReportsController importado")
except Exception as e:
    print(f"   ❌ Error importando ReportsController: {e}")

try:
    from utils.colors import ColorPalette
    print("   ✅ ColorPalette importado")
except Exception as e:
    print(f"   ❌ Error importando ColorPalette: {e}")

# 8. Probar import de reports_view completo
print("\n8. Probando import de ReportsView...")
try:
    # Temporalmente deshabilitar matplotlib si está configurado
    os.environ['DISABLE_MATPLOTLIB'] = '1'
    
    from views.reports_view import ReportsView
    print("   ✅ ReportsView importado correctamente")
except Exception as e:
    print(f"   ❌ Error importando ReportsView: {e}")
    print(f"   Detalles: {str(e)}")
    import traceback
    traceback.print_exc()

# 9. Probar instanciación de ReportsView
print("\n9. Probando creación de ReportsView...")
try:
    reports_view = ReportsView()
    print("   ✅ ReportsView instanciado correctamente")
    
    # Probar mostrar la vista
    reports_view.show()
    print("   ✅ ReportsView mostrado")
    
    # Cerrar inmediatamente
    reports_view.close()
    print("   ✅ ReportsView cerrado")
    
except Exception as e:
    print(f"   ❌ Error instanciando ReportsView: {e}")
    print(f"   Detalles: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("🔍 DIAGNÓSTICO COMPLETADO")
print("Si hay errores arriba, esos son los problemas a resolver.")
