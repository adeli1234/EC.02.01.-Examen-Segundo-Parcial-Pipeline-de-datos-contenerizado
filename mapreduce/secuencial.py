import sys
import time
import pandas as pd

def procesar_secuencial(filepath):
    inicio = time.time()
    
    # Leer CSV omitiendo líneas corruptas
    df = pd.read_csv(filepath, on_bad_lines='skip')
    
    # Limpieza de tipos de datos
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce')
    df = df.dropna(subset=['categoria', 'cantidad', 'precio_unitario'])
    
    # Cálculo y agrupación
    df['total_venta'] = df['cantidad'] * df['precio_unitario']
    resultado = df.groupby('categoria')['total_venta'].sum().round(2)
    
    fin = time.time()
    print(f"--- Resultados Secuenciales (Pandas) ---")
    print(resultado)
    print(f"\nTiempo de ejecución: {fin - inicio:.4f} segundos")

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "/data/input/ventas.csv"
    procesar_secuencial(archivo)