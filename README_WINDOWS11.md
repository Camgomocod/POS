# 🪟 Guía de Instalación Windows 11 - POS RestauranteFast

## 🚀 Instalación Rápida (Recomendada)

### Opción 1: Instalación Automática con PowerShell
```powershell
# Ejecutar como Administrador en PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install_windows11.ps1 -All
```

### Opción 2: Instalación Manual con Batch
```batch
# Doble click en el archivo
POS_Windows11.bat
```

## 📋 Requisitos Previos

### ✅ Python 3.10+ 
- **Descargar**: https://python.org/downloads/
- **⚠️ IMPORTANTE**: Marcar "Add Python to PATH" durante instalación
- **Verificar**: Abrir CMD y ejecutar `py --version`

### ✅ Dependencias Python
Se instalan automáticamente con el script, pero si prefieres manual:
```bash
pip install PyQt5 SQLAlchemy Faker winshell pywin32
```

## 🛠️ Pasos de Instalación Detallados

### Paso 1: Descargar Proyecto
```bash
# Descomprimir ZIP o clonar repositorio
# Navegar a carpeta POS
cd C:\Ruta\A\Tu\Proyecto\POS
```

### Paso 2: Ejecutar Instalador
#### Método A: PowerShell (Recomendado)
1. **Clic derecho** en carpeta → "Abrir en PowerShell"
2. **Ejecutar**: `.\install_windows11.ps1 -All`
3. **Seguir** instrucciones en pantalla

#### Método B: Batch Simple
1. **Doble click** en `POS_Windows11.bat`
2. **Verificar** que abre sin errores

### Paso 3: Verificar Instalación
- ✅ Icono en **Escritorio**: "POS RestauranteFast"
- ✅ Entrada en **Menú Inicio**: Buscar "POS"
- ✅ Archivo **POS_Windows11.bat** funcional

## 🎯 Formas de Ejecutar

### 🖥️ Acceso Directo (Más Fácil)
- **Escritorio**: Doble click en icono "POS RestauranteFast"
- **Menú Inicio**: Buscar "POS RestauranteFast"

### 📁 Archivo Batch
- **Navegar** a carpeta del proyecto
- **Doble click** en `POS_Windows11.bat`

### 💻 Línea de Comandos
```batch
cd C:\Ruta\A\Tu\Proyecto\POS
py main.py
```

## 🔐 Credenciales de Acceso

| Usuario | Contraseña | Permisos |
|---------|------------|----------|
| `admin` | `admin123` | Administrador completo |
| `cajero` | `cajero123` | Operaciones de caja |

## 🔧 Solución de Problemas

### ❌ "Python no encontrado"
```batch
# Verificar instalación
py --version
python --version

# Si no funciona, reinstalar Python:
# 1. Descargar de python.org
# 2. MARCAR "Add to PATH"
# 3. Reiniciar sistema
```

### ❌ "Error de dependencias"
```powershell
# Instalar manualmente
pip install --upgrade pip
pip install PyQt5 SQLAlchemy Faker winshell pywin32
```

### ❌ "No se puede ejecutar scripts PowerShell"
```powershell
# Ejecutar como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ "Aplicación no abre"
1. **Verificar** que `main.py` existe en la carpeta
2. **Comprobar** que `data/pos.db` existe
3. **Ejecutar** desde CMD para ver errores:
   ```batch
   cd C:\Ruta\A\Tu\Proyecto\POS
   py main.py
   ```

## 📊 Testing Semanal Recomendado

### 📅 Día 1-2: Configuración Inicial
- ✅ Login como administrador
- ✅ Crear categorías (Platos, Bebidas, Postres)
- ✅ Añadir productos de prueba
- ✅ Configurar usuarios adicionales

### 📅 Día 3-4: Operaciones de Caja
- ✅ Login como cajero
- ✅ Procesar ventas completas
- ✅ Manejar diferentes métodos de pago
- ✅ Imprimir tickets (si tienes impresora)

### 📅 Día 5-7: Reportes y Administración
- ✅ Generar reportes diarios/semanales
- ✅ Exportar datos CSV
- ✅ Revisar estadísticas de productos
- ✅ Hacer backup de base de datos

## 💾 Backup y Mantenimiento

### Archivos Importantes
```
POS/
├── data/pos.db              # ⭐ BASE DE DATOS (hacer backup)
├── POS_Windows11.bat        # Launcher principal
├── main.py                  # Aplicación principal
└── README_WINDOWS11.md      # Esta guía
```

### Backup Manual
```batch
# Copiar base de datos
copy data\pos.db data\pos_backup_%date%.db

# O usar la función integrada del sistema
# Menú Admin → Gestión de Base de Datos → Exportar
```

## 🚀 Distribución a Otros Equipos

### Para Otros PCs Windows 11:
1. **Copiar** carpeta completa del proyecto
2. **Ejecutar** `install_windows11.ps1` en cada PC
3. **Verificar** credenciales y configuración

### Red Local (Múltiples Cajas):
- Compartir carpeta `data/` en red
- Configurar rutas en `config.py`
- Testing con múltiples usuarios simultáneos

## 📞 Información de Soporte

### Durante Testing (1 semana):
- 📝 **Documentar** problemas encontrados
- ✅ **Probar** todas las funcionalidades
- 💡 **Sugerir** mejoras de UX
- 🐛 **Reportar** bugs específicos

### Post-Testing:
- 🏗️ **Build** final con instalador MSI
- 📦 **Distribución** a producción
- 🔄 **Updates** y mantenimiento

---

## ⚡ Inicio Súper Rápido

```batch
# 1. Descargar proyecto
# 2. Abrir PowerShell en la carpeta
# 3. Ejecutar:
.\install_windows11.ps1 -All

# 4. Doble click en icono del escritorio
# 5. Login: admin / admin123
# 6. ¡Listo para usar! 🎉
```

**¡Perfecto para testing en Windows 11! 🚀**
