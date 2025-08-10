# 🚀 Sistema POS - Guía de Instalación Windows 11

## 📋 Instrucciones de Instalación y Uso

### 🔧 Instalación Automática (Recomendado)

1. **Descargar/Clonar** el proyecto en tu computadora
2. **Ejecutar como Administrador**: `install_pos_w11.bat`
3. **Seguir** las instrucciones en pantalla
4. **Usar** el acceso directo creado en el escritorio

### ⚡ Instalación Manual

```batch
# 1. Verificar requisitos
check_requirements.bat

# 2. Instalar dependencias
install_pos_w11.bat

# 3. Crear accesos directos
PowerShell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1
```

## 📁 Archivos de Instalación

| Archivo                       | Descripción            | Uso                 |
| ----------------------------- | ---------------------- | ------------------- |
| `install_pos_w11.bat`         | Instalador principal   | Primera instalación |
| `run_pos.bat`                 | Ejecutor principal     | Uso diario          |
| `quick_start.bat`             | Inicio rápido          | Usuarios avanzados  |
| `check_requirements.bat`      | Verificar requisitos   | Diagnóstico         |
| `create_desktop_shortcut.ps1` | Crear accesos directos | Configuración       |

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

### Opción 4: Línea de Comandos

```batch
# Activar entorno virtual y ejecutar
cd C:\ruta\a\tu\proyecto\POS
venv\Scripts\activate
python main.py
```

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

### Error: "Python no encontrado"

```batch
# Instalar Python desde python.org
# ✅ Marcar "Add Python to PATH"
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
