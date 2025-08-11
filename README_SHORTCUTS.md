# 🚀 Guía de Instalación y Uso - Accesos Directos POS

## 📋 Descripción General

Este script crea accesos directos para facilitar el uso del Sistema POS sin necesidad de abrir terminal o línea de comandos. Perfecto para testing y uso diario antes del build completo con instalador.

## 🛠️ Instalación de Accesos Directos

### Paso 1: Ejecutar el Script Creador

```bash
# En el directorio del proyecto POS
python create_shortcuts.py
```

El script detectará automáticamente tu sistema operativo y creará los accesos directos apropiados.

### Paso 2: Verificar Creación

#### 🪟 Windows

- **Acceso directo nativo**: Busca "POS RestauranteFast" en el escritorio
- **Archivo .bat**: `POS_RestauranteFast.bat` en la carpeta del proyecto

#### 🐧 Linux

- **Entrada de menú**: Busca "POS RestauranteFast" en el menú de aplicaciones
- **Archivo .desktop**: En `~/.local/share/applications/`
- **Script shell**: `run_pos.sh` en la carpeta del proyecto

#### 🍎 macOS

- **Aplicación**: "POS RestauranteFast.app" en la carpeta Aplicaciones
- **Script shell**: `run_pos.sh` en la carpeta del proyecto

## 🎯 Métodos de Ejecución

### Método 1: Acceso Directo (Recomendado)

- **Windows**: Doble click en el icono del escritorio
- **Linux**: Buscar en menú de aplicaciones o click en escritorio
- **macOS**: Abrir desde carpeta Aplicaciones

### Método 2: Archivos de Lanzamiento

```bash
# Windows
POS_RestauranteFast.bat

# Linux/macOS
./run_pos.sh
```

### Método 3: Terminal (Manual)

```bash
python main.py
```

## 🔐 Credenciales de Acceso

El sistema incluye usuarios predefinidos para testing:

| Usuario  | Contraseña  | Permisos               |
| -------- | ----------- | ---------------------- |
| `admin`  | `admin123`  | Administrador completo |
| `cajero` | `cajero123` | Operaciones de caja    |

## 📁 Estructura de Archivos Generados

```
POS/
├── create_shortcuts.py          # Script creador
├── POS_RestauranteFast.bat     # Launcher Windows
├── run_pos.sh                  # Launcher Unix/Linux/macOS
├── assets/
│   └── pos_icon.ico            # Icono básico
└── data/
    └── pos.db                  # Base de datos mínima (56KB)
```

## 🔧 Solución de Problemas

### Error: "Python no encontrado"

```bash
# Verificar instalación de Python
python --version
# o
python3 --version

# Si usas conda/miniconda
conda activate POS
python --version
```

### Error: "No se puede crear acceso directo en Windows"

```bash
# Instalar dependencias adicionales
pip install winshell pywin32

# Ejecutar nuevamente
python create_shortcuts.py
```

### Error: "Archivo main.py no encontrado"

- Verificar que estás en el directorio correcto del proyecto POS
- Confirmar que `main.py` existe en la carpeta actual

### Error: "Base de datos no encontrada"

```bash
# Recrear base de datos mínima
python tests/create_minimal_db.py
```

## 🎮 Guía de Testing Inicial

### Día 1-2: Configuración Básica

1. **Ejecutar aplicación** usando acceso directo
2. **Login como admin** (admin/admin123)
3. **Configurar categorías** básicas (Platos, Bebidas, etc.)
4. **Añadir productos** de prueba

### Día 3-4: Operaciones de Caja

1. **Login como cajero** (cajero/cajero123)
2. **Procesar pedidos** de prueba
3. **Manejar pagos** (efectivo/tarjeta)
4. **Imprimir tickets** (si tienes impresora)

### Día 5-7: Reportes y Administración

1. **Generar reportes** diarios
2. **Exportar datos** CSV
3. **Gestionar usuarios** adicionales
4. **Backup de base de datos**

## 📊 Funcionalidades Incluidas

### ✅ Módulos Principales

- **👤 Gestión de Usuarios**: Admin y cajeros
- **🍽️ Gestión de Productos**: Categorías, precios, stock
- **🧾 Procesamiento de Pedidos**: POS completo
- **💳 Gestión de Pagos**: Efectivo, tarjeta, mixto
- **📈 Reportes**: Ventas, productos, análisis
- **🖨️ Impresión**: Tickets térmicos
- **💾 Base de Datos**: Backup/restore automático

### ✅ Características Técnicas

- **Interfaz**: PyQt5 optimizada para pantallas pequeñas (1366x768)
- **Base de Datos**: SQLite con SQLAlchemy ORM
- **Ventanas**: Fullscreen automático para uso profesional
- **Exportación**: CSV con resúmenes mensuales
- **Idioma**: Español (interface y reportes)

## 🎯 Próximos Pasos (Post-Testing)

Después de la semana de pruebas:

1. **Recopilar feedback** de uso real
2. **Ajustar configuraciones** según necesidades
3. **Preparar build final** con instalador
4. **Distribución** a otros equipos/locales

## 📞 Soporte

Durante el período de testing, mantén registro de:

- ✅ Funciones que trabajan bien
- ⚠️ Problemas encontrados
- 💡 Mejoras sugeridas
- 🐛 Bugs a corregir

## 🔄 Actualizaciones

Para actualizar el sistema durante el testing:

1. Hacer backup de `data/pos.db`
2. Descargar nueva versión
3. Ejecutar `create_shortcuts.py` nuevamente
4. Restaurar datos si es necesario

---

## ⚡ Inicio Rápido

```bash
# 1. Crear accesos directos
python create_shortcuts.py

# 2. Ejecutar aplicación
# [Usar acceso directo creado]

# 3. Login inicial
# Usuario: admin
# Contraseña: admin123

# 4. ¡Listo para usar!
```

**¡Disfruta tu semana de testing! 🎉**
