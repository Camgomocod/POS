# 🪟 Guía para Windows 11

## 🚀 Ejecución en Windows 11

### ✅ Método Recomendado
```bash
python run_pos_windows11.py
```

### 🔧 Configuración Manual
Si tienes problemas, puedes configurar manualmente:

```python
# En el símbolo del sistema de Windows
set QT_OPENGL=software
set QT_QUICK_BACKEND=software
set PYQTGRAPH_USE_OPENGL=False
python main.py
```

## 🛠️ Solución de Problemas

### ❌ Problema: "Application failed to start"
**Solución:**
```bash
# Reinstalar PyQt5
pip uninstall PyQt5
pip install PyQt5==5.15.9
```

### ❌ Problema: "PyQtGraph crashes"
**Solución:**
```bash
# Forzar software rendering
set QT_OPENGL=software
```

### ❌ Problema: "Interface doesn't open"
**Solución:**
1. Usar `run_pos_windows11.py` en lugar de `main.py`
2. Verificar que no hay procesos Python colgados
3. Reiniciar el equipo si es necesario

## 📋 Dependencias para Windows 11

```txt
PyQt5==5.15.9
pyqtgraph>=0.13.0
SQLAlchemy==1.4.46
pandas>=1.3.0
numpy>=1.21.0
openpyxl>=3.0.0
python-dateutil>=2.8.0
```

## 🎯 Características Optimizadas

- ✅ **Software Rendering**: Sin problemas de OpenGL
- ✅ **Gráficos PyQtGraph**: Reemplazan matplotlib
- ✅ **Formato Colombiano**: Pesos COP sin decimales
- ✅ **Datos Reales**: Sin simulaciones ni datos falsos
- ✅ **Estabilidad**: Configuración específica para Windows 11

## 📞 Soporte

Si sigues teniendo problemas:

1. **Ejecuta diagnóstico:**
   ```bash
   python diagnose_pyqtgraph_windows.py
   ```

2. **Verifica versiones:**
   ```bash
   python -c "import PyQt5; print(PyQt5.Qt.PYQT_VERSION_STR)"
   python -c "import pyqtgraph; print(pyqtgraph.__version__)"
   ```

3. **Logs detallados:**
   ```bash
   python run_pos_windows11.py > debug.log 2>&1
   ```
