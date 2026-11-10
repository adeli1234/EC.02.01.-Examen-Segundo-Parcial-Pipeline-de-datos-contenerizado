from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI(title="DataMart Analytics API")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user="root",
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

class ResultadoSchema(BaseModel):
    categoria: str
    total_ventas: float

@app.get("/resultados")
def obtener_todos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT categoria, total_ventas, fecha_actualizacion FROM resultados_ventas ORDER BY total_ventas DESC;")
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return registros

@app.get("/resultados/{categoria}")
def obtener_por_categoria(categoria: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT categoria, total_ventas, fecha_actualizacion FROM resultados_ventas WHERE LOWER(categoria) = LOWER(%s);", (categoria,))
    registro = cursor.fetchone()
    cursor.close()
    conn.close()
    if not registro:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return registro

@app.post("/resultados", status_code=201)
def crear_o_actualizar(data: ResultadoSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO resultados_ventas (categoria, total_ventas)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE total_ventas = VALUES(total_ventas), fecha_actualizacion = CURRENT_TIMESTAMP;
    """
    cursor.execute(query, (data.categoria, data.total_ventas))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "ok", "categoria": data.categoria, "total_ventas": data.total_ventas}

@app.delete("/resultados/{categoria}")
def eliminar(categoria: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resultados_ventas WHERE LOWER(categoria) = LOWER(%s);", (categoria,))
    affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"status": "eliminado", "categoria": categoria}