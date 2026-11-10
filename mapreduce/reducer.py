#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # Omitir encabezado CSV (insensible a mayúsculas/minúsculas)
    if line.lower().startswith("id,"):
        continue
    
    parts = line.split(",")
    if len(parts) < 8:
        continue
    
    try:
        categoria = parts[3].strip()
        cantidad = int(parts[5].strip())
        precio_unitario = float(parts[6].strip())
        
        total_venta = cantidad * precio_unitario
        
        # Emitir: categoria \t total_venta \t 1 (contador para promediar)
        if categoria:
            print(f"{categoria}\t{total_venta:.2f}\t1")
    except (ValueError, IndexError):
        # Manejo defensivo: ignora líneas mal formadas sin truncar el job
        continue