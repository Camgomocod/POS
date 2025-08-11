# Guía de Solución de Problemas - POS en Windows 11

## 🚨 Problema: La aplicación no abre la interfaz gráfica

### Pasos de Diagnóstico y Solución

#### 1. **Diagnóstico Automático**

```cmd
# Ejecutar el script de diagnóstico
python diagnose_windows.py
```

#### 2. **Modo Debug para Identificar Problemas**

```cmd
# Ejecutar en modo debug para ver detalles
python main_debug.py --debug

# Solo test sin interfaz gráfica
python main_debug.py --no-gui
```

#### 3. **Problemas Comunes y Soluciones**

##### **A. Problema con PyQt5 (NUEVO - Python Microsoft Store)**

```cmd
# Si PyQt5 está instalado pero no se encuentra:
python fix_pyqt5_windows.py

# Ejecutar aplicación con entorno corregido:
run_pos_fixed.bat
# O en PowerShell:
.\run_pos_fixed.ps1
```

**Problema específico de Python del Microsoft Store:**

- Si tienes Python instalado desde Microsoft Store, puede haber problemas con las rutas de paquetes
- Solución recomendada: Instalar Python desde [python.org](https://python.org)

**SOLUCIÓN INMEDIATA para tu caso específico:**

```cmd
# 1. Ejecutar el solucionador automático
python fix_pyqt5_windows.py

# 2. Usar el script generado para ejecutar la app
run_pos_fixed.bat
```

Si el problema persiste, crear entorno virtual:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

##### **B. Problema General con PyQt5**

```cmd
# Desinstalar y reinstalar PyQt5
pip uninstall PyQt5 -y
pip install PyQt5==5.15.9

# Si persiste el problema, probar con conda
conda install pyqt=5.15.9
```

PS C:\Users\vboxuser\POS> python .\diagnose_windows.py
🏥 DIAGNÓSTICO DE POS EN WINDOWS 11
===================================

============================================================
🔍 VERIFICACIÓN DE PYTHON
============================================================
Python Version: 3.13.6
Architecture: 64bit
Platform: Windows-11-10.0.26100-SP0
✅ PASS Python 3.7+
📝 Actual: 3.13

============================================================
🔍 VERIFICACIÓN DE PAQUETES
============================================================
❌ FAIL Package PyQt5
📝 No module named 'pyqt5'
✅ PASS Package sqlalchemy
✅ PASS Package pandas
✅ PASS Package numpy
✅ PASS Package matplotlib
✅ PASS Package openpyxl
❌ FAIL Package pywin32
📝 No module named 'pywin32'

============================================================
🔍 VERIFICACIÓN DE PyQt5
============================================================
✅ PASS PyQt5 import
✅ PASS QApplication creation

============================================================
🔍 VERIFICACIÓN DE PERMISOS
============================================================
✅ PASS Read access: main.py
✅ PASS Read access: config.py
✅ PASS Read access: requirements.txt
❌ FAIL Read access: data/pos.db
📝 'utf-8' codec can't decode byte 0x8a in position 98: invalid start byte

============================================================
🔍 VERIFICACIÓN DE BASE DE DATOS
============================================================
✅ Base de datos ya tiene usuarios, omitiendo inicialización
✅ PASS Database initialization
✅ PASS Database connection

============================================================
🔍 VERIFICACIONES ESPECÍFICAS DE WINDOWS
============================================================
✅ PASS Environment variable PATH
📝 Set (364 chars)
❌ FAIL Environment variable PYTHONPATH
📝 Not set
❌ FAIL Environment variable QT_QPA_PLATFORM_PLUGIN_PATH
📝 Not set
❌ FAIL Visual C++ check
📝 No se pudo verificar

============================================================
🔍 TEST MÍNIMO DE APLICACIÓN
============================================================

##### **B. Falta Visual C++ Redistributable**

- Descargar e instalar: [Visual C++ Redistributable 2015-2019](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- Esto es **CRÍTICO** para PyQt5 en Windows

##### **C. Variables de Entorno**

```cmd
# Configurar variables de entorno para Qt
set QT_QPA_PLATFORM=windows
set QT_AUTO_SCREEN_SCALE_FACTOR=1

# Hacer permanente (PowerShell como administrador)
[Environment]::SetEnvironmentVariable("QT_QPA_PLATFORM", "windows", "User")
[Environment]::SetEnvironmentVariable("QT_AUTO_SCREEN_SCALE_FACTOR", "1", "User")
```

##### **D. Conflictos con Antivirus**

- **Deshabilitar temporalmente** Windows Defender o antivirus
- **Agregar excepción** para la carpeta del proyecto
- **Agregar excepción** para python.exe

##### **E. Permisos de Ejecución**

```cmd
# Ejecutar como administrador
# Clic derecho en CMD → "Ejecutar como administrador"
cd "C:\ruta\al\proyecto\POS"
python main.py
```

#### 4. **Script de Reparación Automática**

```cmd
# Generar y ejecutar script de reparación
python diagnose_windows.py
# Esto creará fix_windows.bat

# Ejecutar como administrador
fix_windows.bat
```

#### 5. **Verificaciones Manuales**

##### **Verificar Python**

```cmd
python --version
# Debe ser 3.7 o superior
```

##### **Verificar PyQt5**

```cmd
python -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 OK')"
```

##### **Verificar Base de Datos**

```cmd
python -c "from utils.database import init_database; init_database(); print('DB OK')"
```

#### 6. **Solución de Último Recurso**

##### **Recrear Entorno Virtual**

```cmd
# Eliminar entorno actual si existe
rmdir /s venv

# Crear nuevo entorno
python -m venv venv
venv\Scripts\activate

# Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Probar aplicación
python main.py
```

##### **Instalación con Conda**

```cmd
# Si pip falla, probar con conda
conda create -n pos_env python=3.9
conda activate pos_env
conda install pyqt=5.15.9 sqlalchemy pandas numpy matplotlib openpyxl
pip install python-dateutil

# Probar aplicación
python main.py
```

### 🔍 Códigos de Error Comunes

| Error                                                  | Causa                      | Solución                             |
| ------------------------------------------------------ | -------------------------- | ------------------------------------ |
| `ImportError: No module named 'PyQt5'`                 | PyQt5 no instalado         | `pip install PyQt5==5.15.9`          |
| `ImportError: DLL load failed`                         | Falta VC++ Redistributable | Instalar VC++ 2015-2019              |
| `qt.qpa.plugin: Could not load the Qt platform plugin` | Variables de entorno       | Configurar `QT_QPA_PLATFORM=windows` |
| Aplicación no aparece pero no da error                 | Antivirus bloqueando       | Deshabilitar antivirus temporalmente |
| `Access denied`                                        | Permisos insuficientes     | Ejecutar como administrador          |

### 📋 Checklist de Solución

- [ ] Python 3.7+ instalado
- [ ] PyQt5==5.15.9 instalado
- [ ] Visual C++ Redistributable 2015-2019 instalado
- [ ] Variables de entorno Qt configuradas
- [ ] Antivirus deshabilitado/excepción agregada
- [ ] Ejecutando como administrador
- [ ] Base de datos inicializada correctamente
- [ ] Sin otras aplicaciones PyQt5 corriendo

### 🆘 Si Nada Funciona

1. **Reportar el problema** con la salida de:

   ```cmd
   python diagnose_windows.py > diagnostico.txt
   python main_debug.py --debug > debug.txt 2>&1
   ```

2. **Información del sistema**:

   ```cmd
   systeminfo > sistema.txt
   pip list > paquetes.txt
   ```

3. **Probar aplicación mínima**:

   ```python
   # test_minimal.py
   from PyQt5.QtWidgets import QApplication, QLabel
   import sys

   app = QApplication(sys.argv)
   label = QLabel("Test PyQt5")
   label.show()
   sys.exit(app.exec_())
   ```

### 🔧 Comandos de Solución Rápida

```cmd
@echo off
echo "🔧 Solución Rápida POS Windows 11"

:: Reinstalar PyQt5
pip uninstall PyQt5 -y
pip install PyQt5==5.15.9

:: Configurar variables
set QT_QPA_PLATFORM=windows
set QT_AUTO_SCREEN_SCALE_FACTOR=1

:: Intentar ejecutar
python main_debug.py --debug

echo "✅ Si persiste el problema, revisar:"
echo "1. Visual C++ Redistributable instalado"
echo "2. Antivirus deshabilitado"
echo "3. Ejecutar como administrador"
pause
```

### 📞 Contacto de Soporte

Si después de seguir todos estos pasos el problema persiste, proporcionar:

- Salida de `diagnose_windows.py`
- Salida de `main_debug.py --debug`
- Información del sistema Windows
- Lista de software antivirus instalado
