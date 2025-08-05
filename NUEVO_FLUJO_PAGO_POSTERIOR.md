# Nuevo Flujo de Trabajo: Pago Posterior al Consumo

## Cambios Implementados

### Flujo Anterior vs Nuevo Flujo

**Anterior (Pago Adelantado):**

```
POS → PENDING → [pago] → PAID → PREPARING → READY → DELIVERED
```

**Nuevo (Pago Posterior):**

```
POS → PENDING → PREPARING → READY → DELIVERED → [pago] → PAID
```

## Modificaciones Realizadas

### 1. POS Window (`views/pos_window.py`)

#### Cambios Principales:

- **Función `process_payment()` → `create_order()`**: Ahora solo crea órdenes, no procesa pagos
- **Botón "💳 Pagar" → "📝 Crear Orden"**: Cambio de texto y funcionalidad
- **CustomerInfoDialog mejorado**: Parámetro `payment_required=False` para órdenes sin pago
- **Mensaje de confirmación actualizado**: Indica que el pago será posterior

#### Código Modificado:

```python
# Crear orden (estado PENDING por defecto)
order = self.order_controller.create_order(
    order_items,
    customer_info['name'],
    customer_info['table']
)

# Imprimir ticket de orden (no recibo de pago)
self.printer.print_order_ticket(order, cart_list)
```

### 2. Kitchen Orders View (`views/kitchen_orders_window.py`)

#### Nuevas Funcionalidades:

- **Botón "💳 Procesar Pago"**: Aparece cuando el estado es `DELIVERED`
- **Señal `payment_requested`**: Para manejar solicitudes de pago
- **Método `handle_payment_request()`**: Abre dialog de pago completo

#### Estados y Botones:

```python
PENDING/PAID → [🚀 Iniciar] → PREPARING
PREPARING → [✅ Listo] → READY
READY → [🚚 Entregar] → DELIVERED
DELIVERED → [💳 Procesar Pago] → PAID
```

#### Filtros Actualizados:

- Todos, Pendientes, Preparando, Listos, **Entregados**, Pagados

#### Prioridades Nuevas:

```python
1. DELIVERED  # Más prioritario - esperando pago
2. READY      # Listos para entregar
3. PREPARING  # En preparación
4. PENDING    # Pendientes de iniciar
5. PAID       # Menos prioritario - ya pagados
```

### 3. Order Controller (`controllers/order_controller.py`)

#### Cambios:

- **`get_active_orders()`**: Incluye `DELIVERED` en órdenes activas
- **`complete_payment()`**: Mantiene funcionalidad para cambiar a `PAID`

```python
def get_active_orders(self):
    return self.db.query(Order).filter(
        Order.status.in_([OrderStatus.PENDING, OrderStatus.PREPARING,
                         OrderStatus.READY, OrderStatus.DELIVERED])
    ).order_by(Order.created_at.asc()).all()
```

### 4. Printer Utility (`utils/printer.py`)

#### Nueva Funcionalidad:

- **`print_order_ticket()`**: Imprime ticket de orden sin información de pago
- **`generate_order_ticket_content()`**: Genera contenido específico para tickets de orden

```python
def print_order_ticket(self, order, cart_items):
    """Generar e imprimir ticket de orden (sin pago)"""
    # Contenido: orden, cliente, items, total, estado pendiente
```

### 5. Customer Info Dialog (`views/pos_window.py`)

#### Mejoras:

- **Parámetro `payment_required`**: Controla si mostrar métodos de pago
- **Tamaño dinámico**: Se ajusta según si requiere pago o no
- **Método `get_customer_info()`**: Opcionalmente incluye método de pago

## Flujo de Trabajo Actualizado

### Para Meseros/Cajeros (POS):

1. Agregar productos al carrito
2. Hacer clic en "📝 Crear Orden"
3. Ingresar datos del cliente y mesa
4. Se genera ticket de orden
5. **NO se procesa pago**

### Para Cocina (Kitchen View):

1. Ver orden en estado "Pendiente"
2. Hacer clic en "🚀 Iniciar" → PREPARING
3. Hacer clic en "✅ Listo" → READY
4. Hacer clic en "🚚 Entregar" → DELIVERED
5. **Hacer clic en "💳 Procesar Pago"** → Abre dialog de pago
6. Completar información de pago → PAID

### Ventajas del Nuevo Flujo:

- ✅ **Más realista**: Los clientes pagan después de consumir
- ✅ **Control de entregas**: Separación clara entre entregado y pagado
- ✅ **Mejor seguimiento**: Estados específicos para cada fase
- ✅ **Flexibilidad**: Órdenes pueden entregarse sin pago inmediato
- ✅ **Menos errores**: No hay presión de pago antes de cocinar

## Archivos Modificados

1. `views/pos_window.py` - POS principal
2. `views/kitchen_orders_window.py` - Vista de cocina
3. `controllers/order_controller.py` - Controlador de órdenes
4. `utils/printer.py` - Utilidad de impresión

## Estado: ✅ IMPLEMENTADO

El nuevo flujo de trabajo está completamente funcional y listo para usar.
