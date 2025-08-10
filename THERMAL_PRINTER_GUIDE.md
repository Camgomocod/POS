# 🖨️ Guía de Impresoras Térmicas USB de 57mm

## 📋 Resumen

Se ha implementado soporte completo para impresoras térmicas USB de 57mm con protocolo ESC/POS para generar recibos automáticamente cuando se procesan pagos en el sistema POS.

## 🎯 Características Implementadas

### ✅ Detección Automática de Impresoras USB

- **Windows**: Utiliza `win32print` para detectar impresoras USB instaladas
- **Linux**: Utiliza CUPS (`pycups`) para detectar impresoras USB del sistema
- **Identificación inteligente**: Detecta automáticamente impresoras térmicas por nombre/modelo

### ✅ Configuración de Impresora

- **Panel de administración**: Nueva pestaña "⚙️ Configuración"
- **Detección en tiempo real**: Lista automática de impresoras USB disponibles
- **Selección fácil**: Tabla con información detallada de cada impresora
- **Configuración persistente**: Se guarda en `printer_config.json`

### ✅ Impresión Térmica Optimizada para 57mm

- **Formato especializado**: Diseño optimizado para papel de 57mm (42 caracteres de ancho)
- **Protocolo ESC/POS**: Comandos nativos para impresoras térmicas
- **Corte automático**: Opción para corte automático de papel
- **Codificación UTF-8**: Soporte para caracteres especiales (ñ, acentos, símbolos)

### ✅ Integración con Sistema POS

- **Impresión automática**: Al confirmar pagos en órdenes de cocina
- **Recibos completos**: Incluye todos los detalles de la orden
- **Métodos de pago**: Iconos y texto para efectivo, transferencia, tarjeta
- **Información del restaurante**: Header personalizable

## 🏗️ Arquitectura Técnica

### 📁 Archivos Principales

#### `utils/printer.py`

- **Clase `ThermalPrinter`**: Manejo principal de impresoras térmicas
- **Detección multiplataforma**: Windows (win32print) y Linux (CUPS)
- **Generación ESC/POS**: Comandos optimizados para papel de 57mm
- **Configuración persistente**: JSON config file

#### `views/printer_config_view.py`

- **Interfaz compacta**: Panel optimizado en 2 columnas para mejor uso del espacio
- **Layout responsivo**: Configuración (izquierda) | Tabla de impresoras (derecha)
- **Botones compactos**: Iconos más pequeños y texto reducido
- **Estado visual**: Indicadores de impresora configurada en formato compacto
- **Configuración en línea**: Parámetros avanzados en una sola fila horizontal

#### `views/kitchen_orders_window.py`

- **Integración de impresión**: Impresión automática al procesar pagos
- **Manejo de errores**: Continúa funcionando aunque falle la impresión
- **Logging**: Información de éxito/error en consola

### 🔧 Especificaciones Técnicas

#### Formato de Recibo (57mm)

```
Ancho de papel: 57mm
Área de impresión: 48mm
Caracteres por línea: 42
Puntos por línea: 384
Velocidad: 70mm/s
```

#### Comandos ESC/POS Utilizados

- **Inicialización**: `ESC @`
- **Corte de papel**: `GS V A 03`
- **Formato de texto**: Bold, subrayado, centrado, doble altura/ancho
- **Fuentes**: Normal, pequeña, doble tamaño

#### Compatibilidad de Impresoras

- Impresoras térmicas con puerto USB
- Protocolo ESC/POS estándar
- Papel de 57mm de ancho
- Marcas compatibles: Epson TM-_, Star RP-_, Bixolon, Citizen, etc.

## 🚀 Uso del Sistema

### 1️⃣ Configuración Inicial

1. **Conectar impresora**: Conecte la impresora térmica USB al sistema
2. **Instalar drivers**: Asegúrese de que los drivers estén instalados
3. **Abrir panel de administración**: Ir a "⚙️ Configuración"
4. **Detectar impresoras**: Hacer clic en "� Buscar" en la columna izquierda
5. **Seleccionar impresora**: Hacer clic en "📌" en la tabla de la derecha
6. **Probar impresión**: Usar "🧪 Test" para verificar funcionamiento
7. **Ajustar configuración**: Modificar ancho y corte en la fila inferior
8. **Guardar**: Hacer clic en "💾 Guardar Configuración"

### 2️⃣ Uso Operativo

1. **Procesar orden**: En órdenes de cocina, seleccionar orden "ready"
2. **Confirmar pago**: Hacer clic en "💳 Procesar Pago"
3. **Llenar información**: Completar datos de cliente y método de pago
4. **Confirmar**: El sistema automáticamente:
   - Procesa el pago
   - Imprime recibo térmico (si hay impresora configurada)
   - Actualiza estado de orden

### 3️⃣ Pruebas y Diagnóstico

```bash
# Ejecutar script de prueba de funcionalidad
python test_thermal_printer.py

# Probar interfaz compacta de configuración
python test_compact_printer_ui.py
```

Los scripts verifican:

- ✅ Detección de impresoras USB
- ✅ Configuración actual
- ✅ Impresión de página de prueba
- ✅ Impresión de recibo real
- ✅ Nueva interfaz compacta y optimizada

## 🔍 Solución de Problemas

### ❌ No se detectan impresoras

**Causas posibles:**

- Impresora no conectada o apagada
- Drivers no instalados
- Impresora no reconocida como USB

**Soluciones:**

1. Verificar conexión física USB
2. Instalar drivers del fabricante
3. Probar impresora con otro software
4. En Linux: verificar permisos CUPS

### ❌ Impresora detectada pero no imprime

**Causas posibles:**

- Papel terminado o mal colocado
- Tapa abierta
- Error de comunicación USB

**Soluciones:**

1. Verificar papel y tapa
2. Reiniciar impresora
3. Probar con "🧪 Probar Impresión"
4. Revisar logs en consola

### ❌ Formato incorrecto en recibo

**Causas posibles:**

- Configuración de ancho incorrecta
- Impresora no compatible con ESC/POS

**Soluciones:**

1. Verificar especificaciones de impresora
2. Ajustar configuración de papel
3. Probar con página de prueba

## 📦 Dependencias

### Requeridas (ya instaladas)

- `PyQt5`: Interfaz gráfica
- `SQLAlchemy`: Base de datos

### Específicas por Plataforma

#### Windows

```bash
pip install pywin32
```

#### Linux

```bash
sudo apt-get install cups-dev
pip install pycups
```

## 📈 Ventajas del Sistema

### ✅ Automático

- Impresión sin intervención manual
- Integrado en flujo de pago existente

### ✅ Robusto

- Continúa funcionando sin impresora
- Manejo de errores elegante

### ✅ Profesional

- Recibos con formato estándar comercial
- Información completa y clara

### ✅ Configurable

- Panel de administración compacto y amigable
- Configuración persistente en formato optimizado

### ✅ Multiplataforma

- Soporte Windows y Linux
- Detección automática de drivers

### ✅ Interfaz Optimizada

- Layout en 2 columnas para mejor aprovechamiento del espacio
- Controles compactos con iconos intuitivos
- Configuración rápida en una sola pantalla

## 🎯 Próximos Pasos Sugeridos

1. **Prueba con impresora real**: Conectar impresora térmica USB de 57mm
2. **Configuración inicial**: Seguir pasos de configuración
3. **Pruebas operativas**: Procesar varios pagos de prueba
4. **Personalización**: Modificar header del restaurante en `printer.py`
5. **Capacitación**: Entrenar personal en uso del sistema

## 📞 Soporte

Para problemas específicos:

1. Ejecutar `python test_thermal_printer.py` para diagnóstico
2. Revisar logs en consola durante operación
3. Verificar configuración en panel de administración
4. Consultar documentación del fabricante de impresora
