#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # Omitir encabezado CSV
    if line.startswith("id,") or line.startswith("ID,"):
        continue
    
    parts = line.split(",")
    if len(parts) < 8:
        continue
    
    try:
        categoria = parts[3].strip()
        cantidad = int(parts[5].strip())
        precio_unitario = float(parts[6].strip())
        
        total_venta = cantidad * precio_unitario
        
        if categoria:
            print(f"{categoria}\t{total_venta:.2f}")
    except (ValueError, IndexError):
        # Manejo defensivo: ignora líneas mal formadas sin truncar el job
        continue