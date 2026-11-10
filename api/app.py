from fastapi import FastAPI, HTTPException
import mysql.connector
import os

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user="root",
        password=os.getenv("MYSQL_ROOT_PASSWORD", "rootpassword"),
        database=os.getenv("MYSQL_DATABASE", "datamart")
    )

@app.get("/resultados")
def get_todos_los_resultados():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resumen_ventas")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return filas

@app.get("/resultados/{categoria}")
def get_resultado_por_categoria(categoria: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resumen_ventas WHERE categoria = %s", (categoria,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()
    if not fila:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return fila

@app.delete("/resultados/{categoria}")
def eliminar_categoria(categoria: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resumen_ventas WHERE categoria = %s", (categoria,))
    conn.commit()
    afectados = cursor.rowcount
    cursor.close()
    conn.close()
    if afectados == 0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada para eliminar")
    return {"mensaje": f"Categoría '{categoria}' eliminada correctamente"}