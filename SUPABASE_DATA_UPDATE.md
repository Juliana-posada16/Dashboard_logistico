# Actualización de Dashboard con Datos de Supabase

## Tablas Disponibles

### 1. datos_pedidos (160 registros)
Contiene información de órdenes con las siguientes columnas:
- Order id
- Fecha
- Documento
- Nombre
- Email
- Teléfono
- Dirección
- Ciudad
- Valor total
- Valor Subtotal
- Valor envio
- IVA
- Valor contraentrega
- Descuento
- Tipo de entrega
- Forma de pago
- Estado
- Fecha entrega
- Piezas
- Guía
- Transportadora

### 2. inventario (45 registros)
Contiene información de stock con las siguientes columnas:
- Código producto
- Producto
- Cantidad

## Datos Muestreados

### Primeros 5 productos del inventario:
1. BOLSA KIT - Código: 1546789-0 - Stock: 2057
2. LIMA SPONGY - Código: 1635465-0 - Stock: 1055
3. COLA DE SIRENA - Código: 1639974-0 - Stock: 1044
4. STICKER DECORACION - Código: 1894053-0 - Stock: 1040
5. MORTERO TRANSPARENTE - Código: 1892818-0 - Stock: 910

## Instrucciones de Actualización

El dashboard HTML actualmente tiene datos embebidos. Para actualizar con datos de Supabase:

1. **Opción 1 (Recomendada)**: Crear un nuevo dashboard que cargue datos dinámicamente desde Supabase
2. **Opción 2**: Reemplazar manualmente el objeto `const DATA = {...}` (líneas 328-4903) en el HTML

## Estructura de datos para el objeto DATA

```javascript
const DATA = {
  "generado_en": "2026-09-04",
  "kpis": {
    "otif_pct": 45.3,
    "pct_novedades_mes": null,
    "pedidos_con_retraso": 22,
    "pedidos_cancelados": 0,
    "tiempo_promedio_transito_dias": 10,
    "total_pedidos": 160,
    "total_pedidos_con_alerta": 38,
    "total_pedidos_dato_incompleto": 0
  },
  "prorateo_mes": { ... },
  "proyeccion_info": { ... },
  "pedidos": [ /* array de 160 pedidos */ ],
  "cobertura_inventario": [ /* array de 45 productos */ ],
  "inventario_kits": [ /* array de kits */ ]
}
```

## Próximos Pasos Recomendados

1. Crear un API endpoint que transforme los datos de Supabase al formato del dashboard
2. Implementar JavaScript en el cliente para cargar datos dinámicamente
3. O generar un nuevo HTML cada vez que se actualice Supabase

## Scripts de Utilidad

Ver los archivos:
- `update_dashboard.py` - Script Python para transformar datos
- `supabase_queries.sql` - Queries SQL para obtener datos
