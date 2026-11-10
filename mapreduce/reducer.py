#!/usr/bin/env python3
import sys

current_categoria = None
total_acumulado = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        categoria, monto_str = line.split("\t", 1)
        monto = float(monto_str)
    except ValueError:
        continue

    if current_categoria == categoria:
        total_acumulado += monto
    else:
        if current_categoria is not None:
            print(f"{current_categoria}\t{total_acumulado:.2f}")
        current_categoria = categoria
        total_acumulado = monto

if current_categoria is not None:
    print(f"{current_categoria}\t{total_acumulado:.2f}")