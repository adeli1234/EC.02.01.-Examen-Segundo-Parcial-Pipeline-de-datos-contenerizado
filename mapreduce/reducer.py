#!/usr/bin/env python3
import sys

current_categoria = None
total_acumulado = 0.0
conteo_total = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        # Se esperan 3 columnas emitidas por el mapper: categoria, monto, conteo
        partes = line.split("\t")
        if len(partes) < 3:
            continue
            
        categoria = partes[0]
        monto = float(partes[1])
        conteo = int(partes[2])
    except ValueError:
        continue

    if current_categoria == categoria:
        total_acumulado += monto
        conteo_total += conteo
    else:
        if current_categoria is not None and conteo_total > 0:
            promedio = total_acumulado / conteo_total
            print(f"{current_categoria}\t{promedio:.2f}")
        current_categoria = categoria
        total_acumulado = monto
        conteo_total = conteo

# Imprimir la última categoría procesada
if current_categoria is not None and conteo_total > 0:
    promedio = total_acumulado / conteo_total
    print(f"{current_categoria}\t{promedio:.2f}")