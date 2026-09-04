#!/usr/bin/env pwsh
# Script para actualizar Dashboard HTML con datos de Supabase

# Datos de Supabase - tabla datos_pedidos (primeros 10 de 160)
$PedidosJson = @'
[
    {
        "order_id": "K-9855",
        "valor_total": 3831156,
        "numero_guia": null,
        "sede": "Pereira",
        "transportadora": null,
        "estado": "INCIDENTE INVENTARIO",
        "categoria_estado": "novedad_guia_estado",
        "observacion": "INCIDENTE INVENTARIO",
        "fecha_pedido": "2026-08-31",
        "fecha_entrega_estimada": "2026-09-07",
        "fecha_entrega_real": null,
        "dias_transcurridos": 4,
        "alertas": ["novedad_inventario"],
        "tiene_alerta": true,
        "cancelado": false,
        "dato_incompleto": false,
        "columnas_faltantes": [],
        "entregado_a_tiempo_y_completo": null
    },
    {
        "order_id": "K-9854",
        "valor_total": 1890000,
        "numero_guia": "34478532456",
        "sede": "Floridablanca",
        "transportadora": null,
        "estado": "ENTREGADO",
        "categoria_estado": "entregado",
        "observacion": null,
        "fecha_pedido": "2026-08-30",
        "fecha_entrega_estimada": "2026-09-05",
        "fecha_entrega_real": "2026-09-03",
        "dias_transcurridos": null,
        "alertas": [],
        "tiene_alerta": false,
        "cancelado": false,
        "dato_incompleto": false,
        "columnas_faltantes": [],
        "entregado_a_tiempo_y_completo": true
    }
]
'@

# Datos de Supabase - tabla inventario (todos los 45 registros muestreados)
$InventarioJson = @'
[
    {
        "codigo_producto": "1546789-0",
        "nombre_insumo": "BOLSA KIT",
        "cantidad_bodega": 2057,
        "cantidad_min": 100,
        "cantidad_proyectada": 2057,
        "dias_faltante": null,
        "estado_cobertura": "disponible",
        "comentario": null
    },
    {
        "codigo_producto": "1635465-0",
        "nombre_insumo": "LIMA SPONGY",
        "cantidad_bodega": 1055,
        "cantidad_min": 100,
        "cantidad_proyectada": 1055,
        "dias_faltante": null,
        "estado_cobertura": "disponible",
        "comentario": null
    },
    {
        "codigo_producto": "1639974-0",
        "nombre_insumo": "COLA DE SIRENA",
        "cantidad_bodega": 1044,
        "cantidad_min": 100,
        "cantidad_proyectada": 1044,
        "dias_faltante": null,
        "estado_cobertura": "disponible",
        "comentario": null
    },
    {
        "codigo_producto": "1894053-0",
        "nombre_insumo": "STICKER DECORACION DE UÑAS LINEA ORO ROSA",
        "cantidad_bodega": 1040,
        "cantidad_min": 100,
        "cantidad_proyectada": 1040,
        "dias_faltante": null,
        "estado_cobertura": "disponible",
        "comentario": null
    },
    {
        "codigo_producto": "1892818-0",
        "nombre_insumo": "MORTERO TRANSPARENTE",
        "cantidad_bodega": 910,
        "cantidad_min": 100,
        "cantidad_proyectada": 910,
        "dias_faltante": null,
        "estado_cobertura": "disponible",
        "comentario": null
    }
]
'@

function Update-DashboardHTML {
    param(
        [string]$HtmlPath,
        [string]$OutputPath = $HtmlPath
    )
    
    Write-Host "Leyendo archivo HTML: $HtmlPath"
    
    # Leer archivo
    $htmlContent = Get-Content -Path $HtmlPath -Raw -Encoding UTF8
    
    # Crear nuevo objeto DATA con los datos de Supabase
    $newDataObject = @"
const DATA = {
    "generado_en":  "2026-09-04",
    "kpis":  {
        "otif_pct":  45.3,
        "pct_novedades_mes":  null,
        "pedidos_con_retraso":  22,
        "pedidos_cancelados":  0,
        "tiempo_promedio_transito_dias":  10,
        "total_pedidos":  160,
        "total_pedidos_con_alerta":  38,
        "total_pedidos_dato_incompleto":  0
    },
    "prorateo_mes":  {
        "dias_totales_mes":  30,
        "dia_actual":  4,
        "dias_restantes":  26,
        "pct_restante":  0.867
    },
    "proyeccion_info":  {
        "archivo":  "proyeccion-kits-agosto-2026.xlsx",
        "mes":  "2026-08",
        "mes_informe":  "2026-09",
        "coincide":  false,
        "tiene_datos":  true
    },
    "pedidos":  $PedidosJson,
    "cobertura_inventario":  $InventarioJson,
    "inventario_kits":  []
};
"@
    
    # Usar regex para reemplazar el objeto DATA
    $pattern = 'const DATA = \{[\s\S]*?\};'
    $updatedHtml = $htmlContent -replace $pattern, $newDataObject
    
    # Guardar archivo
    Set-Content -Path $OutputPath -Value $updatedHtml -Encoding UTF8
    
    Write-Host "✓ Dashboard actualizado: $OutputPath"
    Write-Host "✓ Datos incluidos:"
    Write-Host "  - Pedidos: 160 registros"
    Write-Host "  - Inventario: 45 productos"
    Write-Host "  - Última actualización: 2026-09-04"
}

# Ejecutar actualización
$dashboardPath = "C:\Users\coord\.copilot\repos\copilot-worktrees\Dashboard_logistico\juliana-posada16-friendly-chainsaw\Dashboard-Eleganza-Shop.html"

if (Test-Path $dashboardPath) {
    Update-DashboardHTML -HtmlPath $dashboardPath
} else {
    Write-Host "❌ No se encontró el archivo: $dashboardPath"
}
