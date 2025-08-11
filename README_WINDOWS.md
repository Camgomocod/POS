# 🚀 Sistema POS - Guía de Instalación Windows 11

## 📋 Instrucciones de Instalación y Uso

### 🔧 Instalación Automática (Recomendado)

1. **Descargar/Clonar** el proyecto en tu computadora
2. **IMPORTANTE**: Extraer en una ruta SIN ESPACIOS (ej: `C:\POS\`)
3. **Ejecutar como Administrador**: `install_pos_simple.bat`
4. **Seguir** las instrucciones en pantalla
5. **Crear acceso directo**: Ejecutar `create_shortcut_simple.bat`

### ⚡ Instalación Manual

cd ..

```batch
# 1. Verificar requisitos
check_requirements.bat

# 2. Instalar dependencias (VERSIÓN SIMPLE)
install_pos_simple.bat

# 3. Crear accesos directos
create_shortcut_simple.bat
```

### 🚨 Solución al Error de Caracteres Especiales

Si ves errores como "no se reconoce como comando":

1. **Extraer el proyecto** en una ruta SIN ESPACIOS

   - ✅ Correcto: `C:\POS\`
   - ✅ Correcto: `C:\Proyectos\POS\`
   - ❌ Incorrecto: `C:\Users\Usuario\Downloads\POS-main\`

2. **Usar la versión simplificada**:

   ```batch
   install_pos_simple.bat
   ```

3. **Crear acceso directo separadamente**:
   ```batch
   create_shortcut_simple.bat
   ```

## 📁 Archivos de Instalación

| Archivo                      | Descripción                          | Uso                   |
| ---------------------------- | ------------------------------------ | --------------------- |
| `fix_access_violation.bat`   | Solución Access Violation (NUEVO)    | Error -1073741819     |
| `main_safe.py`               | Sistema sin gráficos (NUEVO)         | Modo seguro           |
| `fix_dependencies.bat`       | Solución rápida dependencias (NUEVO) | Error matplotlib      |
| `install_pos_simple.bat`     | Instalador principal (NUEVO)         | Primera instalación   |
| `launcher_windows.bat`       | Ejecutor especial (NUEVO)            | Problemas PyQt5       |
| `diagnostico_sistema.bat`    | Diagnóstico completo (NUEVO)         | Identificar problemas |
| `solucionador_problemas.bat` | Solucionador automático (NUEVO)      | Reparar problemas     |
| `test_pyqt5_simple.py`       | Prueba rápida PyQt5 (NUEVO)          | Test GUI mínimo       |
| `test_pyqt5.py`              | Probar PyQt5                         | Verificar GUI         |
| `install_pos_w11.bat`        | Instalador completo                  | Instalación avanzada  |
| `run_pos.bat`                | Ejecutor principal                   | Uso diario            |
| `quick_start.bat`            | Inicio rápido                        | Usuarios avanzados    |
| `check_requirements.bat`     | Verificar requisitos                 | Diagnóstico           |
| `create_shortcut_simple.bat` | Crear accesos directos (NUEVO)       | Configuración         |

## 🎯 Formas de Ejecutar el Sistema

### Opción 1: Acceso Directo (Recomendado)

- Doble clic en **"Sistema POS"** en el escritorio
- Se ejecutan todas las verificaciones automáticamente

### Opción 2: Desde Carpeta del Proyecto

```batch
# Navegar a la carpeta del proyecto
cd C:\ruta\a\tu\proyecto\POS

# Ejecutar
run_pos.bat
```

### Opción 3: Inicio Rápido

- Doble clic en **"Sistema POS - Inicio Rápido"**
- Omite verificaciones (más rápido)

### Opción 4: Launcher Especial (NUEVO - Para Problemas)

```batch
# Para problemas con python main.py
launcher_windows.bat
```

### Opción 5: Modo Seguro (NUEVO - Para Access Violation)

```batch
# Para error -1073741819 o crashes gráficos
python main_safe.py
# O usar:
run_pos_safe.bat
```

### Opción 6: Test Rápido PyQt5 (NUEVO - Verificación)

```batch
# Para verificar que PyQt5 funciona antes del sistema completo
python test_pyqt5_simple.py
```

**💡 Si este test funciona, PyQt5 está bien configurado y puedes usar el sistema completo.**

### Opción 7: Línea de Comandos

```batch
# Activar entorno virtual y ejecutar
cd C:\ruta\a\tu\proyecto\POS
venv\Scripts\activate
python main.py
```

## 🚨 ¿python main.py no funciona?

Si `python main.py` no abre ninguna ventana:

### Diagnóstico Rápido

```batch
# 1. Ejecutar diagnóstico
diagnostico_sistema.bat

# 2. Probar PyQt5 específicamente
python test_pyqt5.py

# 3. Usar launcher especial
launcher_windows.bat

# 4. Solucionador automático
solucionador_problemas.bat
```

### 🔧 Solución al Error de Dependencias Faltantes

**Error más común**: `ModuleNotFoundError: No module named 'matplotlib'`

```batch
# SOLUCIÓN RÁPIDA:
# 1. Activar entorno virtual
venv\Scripts\activate

# 2. Instalar dependencias faltantes
pip install matplotlib>=3.5.0
pip install pywin32>=304
pip install numpy>=1.21.0

# 3. O reinstalar todas las dependencias
pip install -r requirements.txt --force-reinstall
```

### Causas Comunes:

- **Dependencies incompletas**: Usar `pip install -r requirements.txt`
- **matplotlib faltante**: Ejecutar `solucionador_problemas.bat` → opción 1
- **win32print faltante**: Ejecutar `solucionador_problemas.bat` → opción 2
- **PyQt5 mal instalado**: Usar `pip install --force-reinstall PyQt5`
- **Entorno gráfico**: Windows bloquea aplicaciones GUI desde consola
- **Ruta con espacios**: Mover proyecto a `C:\POS\`

## 👤 Credenciales por Defecto

```
🔐 ADMINISTRADOR
Usuario: admin
Contraseña: admin123
Acceso: Gestión completa

🔐 CAJERO
Usuario: cajero
Contraseña: cajero123
Acceso: POS y operaciones básicas
```

## 🔍 Solución de Problemas

### Error: "Python: can't open file" o "no se reconoce como comando"

```batch
# CAUSA: Ruta con espacios o caracteres especiales
# SOLUCIÓN:
# 1. Mover proyecto a ruta simple: C:\POS\
# 2. Usar versión simplificada:
install_pos_simple.bat
```

### Error: "ModuleNotFoundError: No module named 'matplotlib'"

```batch
# SOLUCIÓN INMEDIATA:
# 1. Activar entorno virtual
cd C:\POS
venv\Scripts\activate

# 2. Instalar matplotlib y dependencias
pip install matplotlib>=3.5.0
pip install pywin32>=304
pip install numpy>=1.21.0

# 3. Probar ejecución
python main.py

# ALTERNATIVA AUTOMÁTICA:
solucionador_problemas.bat
# Seleccionar opción 1 (matplotlib) o 5 (todas las dependencias)
```

### Error: Código -1073741819 (Access Violation)

```batch
# SOLUCIÓN ESPECÍFICA PARA ACCESS VIOLATION:
# 1. Ejecutar script de solución automática
fix_access_violation.bat

# 2. ALTERNATIVA: Usar modo seguro (sin gráficos)
python main_safe.py

# 3. O usar launcher seguro
run_pos_safe.bat

# El error -1073741819 es común con PyQt5 + matplotlib en Windows
# Estas soluciones configuran el entorno correctamente
```

### Error: "Platform-specific printing modules not available"

```batch
# Instalar módulos de impresión para Windows
pip install pywin32>=304

# Si persiste el error, es solo una advertencia
# El sistema funcionará sin problemas de impresión
```

### Error: "Módulo no encontrado"

```batch
# Reinstalar dependencias
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Base de datos no encontrada"

```batch
# Verificar base de datos
python verify_clean_database.py
```

### Error: "Permisos insuficientes"

```batch
# Ejecutar como administrador
# Clic derecho → "Ejecutar como administrador"
```

### Error: PowerShell ExecutionPolicy

```batch
# Usar versión VBS en lugar de PowerShell:
create_shortcut_simple.bat
```

## 📊 Verificación de Instalación

### Test Rápido

```batch
# Verificar Python
python --version

# Verificar dependencias
pip list | findstr "PyQt5 SQLAlchemy"

# Probar aplicación
quick_start.bat
```

### Test Completo

```batch
# Verificar todos los requisitos
check_requirements.bat

# Verificar base de datos
python verify_clean_database.py

# Ejecutar con verificaciones completas
run_pos.bat
```

## 📝 Requisitos del Sistema

### Mínimos

- Windows 10/11
- Python 3.7 o superior
- 500 MB espacio libre
- 2 GB RAM

### Recomendados

- Windows 11
- Python 3.9 o superior
- 1 GB espacio libre
- 4 GB RAM
- Conexión a internet (para instalación)

## 🎯 Primeros Pasos Después de la Instalación

### 1. Login Inicial

- Usar credenciales de administrador: `admin/admin123`

### 2. Configuración Básica

1. **Ir a Administración** → Gestión de Productos
2. **Crear categorías** según tu restaurante
3. **Agregar productos** con precios reales
4. **Configurar usuarios** adicionales si es necesario

### 3. Pruebas Operacionales

1. **Login como cajero**: `cajero/cajero123`
2. **Probar POS**: Agregar productos, calcular totales
3. **Procesar órdenes**: Crear órdenes de prueba
4. **Revisar cocina**: Ver órdenes pendientes
5. **Procesar pagos**: Completar transacciones

## ⚠️ Importante para Producción

- **Cambiar contraseñas** por defecto
- **Configurar datos** del restaurante en `config.py`
- **Hacer respaldo** de la base de datos regularmente
- **Probar impresoras** térmicas si las usas
- **Capacitar personal** en el uso del sistema

## 🆘 Soporte

### Archivos de Log

- Revisar la consola durante la ejecución
- Errores se muestran en tiempo real

### Reinstalación Completa

```batch
# 1. Eliminar entorno virtual
rmdir /s /q venv

# 2. Reinstalar
install_pos_w11.bat
```

### Contacto

- Revisar documentación en `/docs/`
- Verificar issues conocidos
- Consultar `SISTEMA_LISTO_TESTING.md`

---

## ✅ Estado del Sistema

Según `SISTEMA_LISTO_TESTING.md`:

- ✅ Base de datos limpia (56 KB)
- ✅ Usuarios básicos configurados
- ✅ Sistema probado y funcionando
- ✅ Listo para testing con datos reales
- ✅ Preparado para uso en producción

**¡El sistema está completamente listo para usar!**
