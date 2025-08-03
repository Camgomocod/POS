# POS

POS - Fast Restaurant Point of Sale (POS) System

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características Principales](#características-principales)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Documentación](#documentación)

## Descripción

Este proyecto es un sistema de punto de venta (POS) para restaurantes, desarrollado en Python con una arquitectura MVC. Permite gestionar usuarios, productos, categorías, pedidos y pagos a través de una interfaz gráfica basada en Qt.

## Características Principales

1. **Autenticación de Usuarios**

   - Interfaz de login con validación de credenciales.
   - Control de roles (administrador, cajero, cocina).

2. **Interfaz Principal**

   - Ventana principal para navegación de módulos.
   - Acceso rápido a funciones de venta y administración.

3. **Punto de Venta (POS)**

   - Vista de productos con distribución responsiva (3-6 columnas según resolución).
   - Carrito de compra con cálculo de totales y distribución 70/30.
   - Gestión de categorías y filtros dinámicos.

4. **Gestión de Pedidos**

   - Creación y seguimiento de pedidos.
   - Vista de pedidos en cocina (estado pendiente, en preparación, finalizado).
   - Historial de pagos y reporte de ventas.

5. **Administración**

   - Ventana de administración para CRUD de usuarios, productos y categorías.
   - Control de acceso según rol de usuario.

6. **Migración y Base de Datos**

   - Script `migrate_db.py` para inicializar y actualizar la base de datos SQLite.
   - Módulo `database.py` para conexión y gestión de transacciones.

7. **Utilidades**
   - `colors.py`: Colores y estilos para la consola.
   - `printer.py`: Generación de tickets o informes en PDF/impresión.

## Estructura del Proyecto

```
config.py
main.py
migrate_db.py
controllers/
  ├─ auth_controller.py
  ├─ product_controller.py
  ├─ order_controller.py
  ├─ payment_controller.py
  ├─ report_controller.py
  └─ app_controller.py
models/
  ├─ user.py
  ├─ base.py
  ├─ category.py
  ├─ product.py
  ├─ order.py
  └─ order_item.py
utils/
  ├─ database.py
  ├─ colors.py
  └─ printer.py
views/
  ├─ login_window.py
  ├─ main_window.py
  ├─ pos_window.py
  ├─ admin_window.py
  ├─ kitchen_orders_window.py
  └─ payment_history_window.py
data/
  └─ pos.db
```

## Instalación y Ejecución

1. Clonar el repositorio:
   ```bash
   git clone <repo-url>
   cd POS
   ```
2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Inicializar la base de datos:
   ```bash
   python migrate_db.py
   ```
4. Ejecutar la aplicación:
   ```bash
   python main.py
   ```

## Documentación

- **MEJORAS_DISTRIBUCION.md**: Detalles de la distribución responsiva de la interfaz POS.
- **README.md**: Visión general y guías de uso.
