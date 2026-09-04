#!/usr/bin/env python3
"""
Script para actualizar el Dashboard de Eleganza Shop con datos de Supabase
Transforma los datos de las tablas datos_pedidos e inventario al formato JSON del dashboard
"""

import json
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# Datos de pedidos desde Supabase (tabla datos_pedidos)
PEDIDOS_RAW = [
    {"Order id": "K-9855", "Fecha": "2026-08-31", "Nombre": "CEINDER S.A.S", "Valor total": "3831156", "Estado": "INCIDENTE INVENTARIO", "Ciudad": "Pereira"},
    {"Order id": "K-9854", "Fecha": "2026-08-30", "Nombre": "Cliente B", "Valor total": "1890000", "Estado": "ENTREGADO", "Ciudad": "Floridablanca"},
    # ... más pedidos
]

# Datos de inventario desde Supabase (tabla inventario)
INVENTARIO_RAW = [
    {"Código producto": "1546789-0", "Producto": "BOLSA KIT", "Cantidad": 2057},
    {"Código producto": "1635465-0", "Producto": "LIMA SPONGY", "Cantidad": 1055},
    # ... más productos
]

def transform_pedidos_data():
    """Transforma datos de pedidos al formato del dashboard"""
    pedidos_transformados = []
    
    for p in PEDIDOS_RAW:
        pedido = {
            "order_id": p.get("Order id", ""),
            "valor_total": int(p.get("Valor total", 0)),
            "numero_guia": p.get("Guía"),
            "sede": p.get("Ciudad", ""),
            "transportadora": p.get("Transportadora"),
            "estado": p.get("Estado", ""),
            "categoria_estado": categorize_estado(p.get("Estado", "")),
            "observacion": None,
            "fecha_pedido": p.get("Fecha", ""),
            "fecha_entrega_estimada": p.get("Fecha entrega", ""),
            "fecha_entrega_real": None,
            "dias_transcurridos": calculate_dias(p.get("Fecha", "")),
            "alertas": check_alertas(p),
            "tiene_alerta": has_alerta(p),
            "cancelado": p.get("Estado", "").upper() == "CANCELADO",
            "dato_incompleto": False,
            "columnas_faltantes": [],
            "entregado_a_tiempo_y_completo": None
        }
        pedidos_transformados.append(pedido)
    
    return pedidos_transformados

def categorize_estado(estado):
    """Categoriza el estado del pedido"""
    estado = estado.upper()
    if "ENTREGADO" in estado:
        return "entregado"
    elif "CANCELADO" in estado:
        return "cancelado"
    elif "INCIDENTE" in estado:
        return "novedad_guia_estado"
    elif "TRANSITO" in estado:
        return "transito_nacional"
    else:
        return "pendiente_alistamiento"

def calculate_dias(fecha_str):
    """Calcula días transcurridos desde la fecha del pedido"""
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        hoy = datetime(2026, 9, 4)  # Fecha actual del dashboard
        dias = (hoy - fecha).days
        return dias if dias > 0 else 0
    except:
        return 0

def check_alertas(pedido):
    """Verifica alertas en el pedido"""
    alertas = []
    if pedido.get("Estado", "").upper() == "INCIDENTE INVENTARIO":
        alertas.append("novedad_inventario")
    return alertas

def has_alerta(pedido):
    """Verifica si el pedido tiene alerta"""
    return len(check_alertas(pedido)) > 0

def transform_inventario_data():
    """Transforma datos de inventario"""
    inventario_transformado = []
    
    for item in INVENTARIO_RAW:
        inv = {
            "codigo_producto": item.get("Código producto", ""),
            "producto": item.get("Producto", ""),
            "cantidad_bodega": item.get("Cantidad", 0),
            "cantidad_min": 100,  # Valor por defecto
            "cantidad_proyectada": item.get("Cantidad", 0),
            "dias_faltante": None,
            "estado_cobertura": "disponible" if item.get("Cantidad", 0) > 100 else "reabastecer",
            "comentario": None
        }
        inventario_transformado.append(inv)
    
    return inventario_transformado

def generate_kpis(pedidos):
    """Genera KPIs basados en pedidos"""
    total_pedidos = len(pedidos)
    pedidos_entregados = sum(1 for p in pedidos if p["categoria_estado"] == "entregado")
    pedidos_con_alerta = sum(1 for p in pedidos if p["tiene_alerta"])
    pedidos_cancelados = sum(1 for p in pedidos if p["cancelado"])
    
    otif_pct = (pedidos_entregados / total_pedidos * 100) if total_pedidos > 0 else 0
    
    return {
        "otif_pct": round(otif_pct, 1),
        "pct_novedades_mes": None,
        "pedidos_con_retraso": sum(1 for p in pedidos if p["dias_transcurridos"] > 6),
        "pedidos_cancelados": pedidos_cancelados,
        "tiempo_promedio_transito_dias": 10,
        "total_pedidos": total_pedidos,
        "total_pedidos_con_alerta": pedidos_con_alerta,
        "total_pedidos_dato_incompleto": 0
    }

def main():
    """Genera el objeto DATA completo"""
    
    # Transformar datos
    pedidos = transform_pedidos_data()
    inventario = transform_inventario_data()
    kpis = generate_kpis(pedidos)
    
    # Construir objeto DATA
    data = {
        "generado_en": "2026-09-04",
        "kpis": kpis,
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
        "pedidos": pedidos,
        "cobertura_inventario": inventario,
        "inventario_kits": []
    }
    
    # Salida formateada
    output = json.dumps(data, indent=2, ensure_ascii=False)
    print(output)
    
    # Guardar en archivo temportal
    with open("dashboard_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Datos procesados: {len(pedidos)} pedidos, {len(inventario)} productos", file=__import__("sys").stderr)

if __name__ == "__main__":
    main()
