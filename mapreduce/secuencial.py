#!/usr/bin/env python3
import sys
import time
import pandas as pd

def procesar_secuencial(filepath):
    start_time = time.time()
    
    df = pd.read_csv(filepath, on_bad_lines='skip')
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce')
    df = df.dropna(subset=['categoria', 'cantidad', 'precio_unitario'])
    
    df['total_venta'] = df['cantidad'] * df['precio_unitario']
    resultado = df.groupby('categoria')['total_venta'].sum().round(2)
    
    end_time = time.time()
    print("=== RESULTADO SECUENCIAL (PANDAS) ===")
    print(resultado)
    print(f"\nTiempo de ejecución: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 secuencial.py <ruta_csv>")
        sys.exit(1)
    procesar_secuencial(sys.argv[1])