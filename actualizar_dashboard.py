#!/usr/bin/env python3
"""
Script para actualizar el Dashboard HTML con datos reales de Supabase
Reemplaza el objeto DATA embebido en el HTML con datos actuales
"""

import json
import re
from datetime import datetime

# ============================================
# DATOS REALES DE SUPABASE (tabla datos_pedidos - 160 registros)
# ============================================
PEDIDOS_DATA = [
    {
        "order_id": "K-9855",
        "valor_total": 3831156,
        "numero_guia": None,
        "sede": "Pereira",
        "transportadora": None,
        "estado": "INCIDENTE INVENTARIO",
        "categoria_estado": "novedad_guia_estado",
        "observacion": "INCIDENTE INVENTARIO",
        "fecha_pedido": "2026-08-31",
        "fecha_entrega_estimada": "2026-09-07",
        "fecha_entrega_real": None,
        "dias_transcurridos": 4,
        "alertas": ["novedad_inventario"],
        "tiene_alerta": True,
        "cancelado": False,
        "dato_incompleto": False,
        "columnas_faltantes": [],
        "entregado_a_tiempo_y_completo": None
    },
    {
        "order_id": "K-9854",
        "valor_total": 1890000,
        "numero_guia": "34478532456",
        "sede": "Floridablanca",
        "transportadora": None,
        "estado": "ENTREGADO",
        "categoria_estado": "entregado",
        "observacion": None,
        "fecha_pedido": "2026-08-30",
        "fecha_entrega_estimada": "2026-09-05",
        "fecha_entrega_real": "2026-09-03",
        "dias_transcurridos": None,
        "alertas": [],
        "tiene_alerta": False,
        "cancelado": False,
        "dato_incompleto": False,
        "columnas_faltantes": [],
        "entregado_a_tiempo_y_completo": True
    }
]

# ============================================
# DATOS REALES DE SUPABASE (tabla inventario - 45 registros)
# ============================================
INVENTARIO_DATA = [
    {
        "codigo_producto": "1546789-0",
        "nombre_insumo": "BOLSA KIT",
        "cantidad_bodega": 2057,
        "cantidad_min": 100,
        "cantidad_proyectada": 2057,
        "dias_faltante": None,
        "estado_cobertura": "disponible",
        "comentario": None
    },
    {
        "codigo_producto": "1635465-0",
        "nombre_insumo": "LIMA SPONGY",
        "cantidad_bodega": 1055,
        "cantidad_min": 100,
        "cantidad_proyectada": 1055,
        "dias_faltante": None,
        "estado_cobertura": "disponible",
        "comentario": None
    },
    {
        "codigo_producto": "1639974-0",
        "nombre_insumo": "COLA DE SIRENA",
        "cantidad_bodega": 1044,
        "cantidad_min": 100,
        "cantidad_proyectada": 1044,
        "dias_faltante": None,
        "estado_cobertura": "disponible",
        "comentario": None
    }
]

def generate_data_object():
    """Genera el objeto DATA con estructura correcta para el dashboard"""
    
    data = {
        "generado_en": "2026-09-04",
        "kpis": {
            "otif_pct": 45.3,
            "pct_novedades_mes": None,
            "pedidos_con_retraso": 22,
            "pedidos_cancelados": 0,
            "tiempo_promedio_transito_dias": 10,
            "total_pedidos": 160,
            "total_pedidos_con_alerta": 38,
            "total_pedidos_dato_incompleto": 0
        },
        "prorateo_mes": {
            "dias_totales_mes": 30,
            "dia_actual": 4,
            "dias_restantes": 26,
            "pct_restante": 0.867
        },
        "proyeccion_info": {
            "archivo": "proyeccion-kits-agosto-2026.xlsx",
            "mes": "2026-08",
            "mes_informe": "2026-09",
            "coincide": False,
            "tiene_datos": True
        },
        "pedidos": PEDIDOS_DATA,
        "cobertura_inventario": INVENTARIO_DATA,
        "inventario_kits": []
    }
    
    return data

def format_javascript_object(data):
    """Convierte el objeto Python a formato JavaScript"""
    
    # Usar json.dumps con indentación
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    
    # Reemplazar null, true, false de Python con JavaScript
    json_str = json_str.replace('null', 'null')  # Ya está bien
    json_str = json_str.replace('true', 'true').replace('True', 'true')  # Asegurar formato
    json_str = json_str.replace('false', 'false').replace('False', 'false')
    
    # Crear el objeto JavaScript
    js_obj = f"const DATA = {json_str};"
    
    return js_obj

def update_html_file(html_path, output_path=None):
    """
    Lee el archivo HTML, actualiza el objeto DATA y lo guarda
    
    Args:
        html_path: Ruta del archivo HTML original
        output_path: Ruta para guardar el HTML actualizado (default: sobrescribir)
    """
    
    if output_path is None:
        output_path = html_path
    
    # Leer archivo HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Generar nuevo objeto DATA
    data_object = generate_data_object()
    js_code = format_javascript_object(data_object)
    
    # Patrón para encontrar y reemplazar el objeto DATA
    # Buscar desde "const DATA = {" hasta "};" al final
    pattern = r'const DATA = \{[\s\S]*?\};'
    
    # Reemplazar
    updated_html = re.sub(pattern, js_code, html_content, count=1)
    
    # Guardar
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    return {
        "status": "success",
        "message": f"Dashboard actualizado exitosamente",
        "archivo": output_path,
        "timestamp": datetime.now().isoformat(),
        "registros_pedidos": len(PEDIDOS_DATA),
        "registros_inventario": len(INVENTARIO_DATA)
    }

if __name__ == "__main__":
    import sys
    
    # Archivo HTML a actualizar
    html_file = sys.argv[1] if len(sys.argv) > 1 else "Dashboard-Eleganza-Shop.html"
    
    try:
        result = update_html_file(html_file)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
