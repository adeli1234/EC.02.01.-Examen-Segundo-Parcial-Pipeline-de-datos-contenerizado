import os
import mysql.connector

def cargar():
    host = os.getenv("MYSQL_HOST", "db")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = "root"
    password = os.getenv("MYSQL_ROOT_PASSWORD")
    database = os.getenv("MYSQL_DATABASE")

    file_path = "/data/output/resultado/part-00000"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} no existe.")
        return

    conn = mysql.connector.connect(
        host=host, port=port, user=user, password=password, database=database
    )
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_ventas (
            categoria VARCHAR(100) PRIMARY KEY,
            total_ventas DECIMAL(15,2) NOT NULL,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
    """)

    query = """
        INSERT INTO resultados_ventas (categoria, total_ventas)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE total_ventas = VALUES(total_ventas);
    """

    count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                cursor.execute(query, (parts[0], float(parts[1])))
                count += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Se cargaron correctamente {count} registros en MySQL.")

if __name__ == "__main__":
    cargar()