# EC.02.01.-Examen-Segundo-Parcial-Pipeline-de-datos-contenerizado

## Examen P2 - 125052910

## Parte E. Teoría

### E1. Modos de Hadoop y uso de HDFS
Hadoop opera en tres modos principales:
1. **Standalone (Local):** Se ejecuta en un solo proceso JVM sobre el sistema de archivos local del sistema operativo host; no inicia demonios ni utiliza HDFS.
2. **Pseudo-distribuido:** Todos los demonios de Hadoop (NameNode, DataNode, ResourceManager, NodeManager) se ejecutan dentro de una sola máquina/contenedor.
3. **Totalmente distribuido:** Los demonios se dividen y ejecutan a través de un clúster físico o virtual de múltiples nodos independientes.

**Respuesta a HDFS:** HDFS únicamente se utiliza en los modos **pseudo-distribuido** y **totalmente distribuido**.

---

### E2. Montaje del dataset mediante Volumen vs. COPY
Se utiliza un volumen en lugar de la instrucción `COPY` por dos razones fundamentales:
1. **Eficiencia y peso de la imagen:** Copiar datasets de gran tamaño incrementa drásticamente el tamaño final de la imagen Docker y alarga los tiempos de construcción (`docker build`).
2. **Flexibilidad en tiempo de desarrollo:** Montar el archivo como volumen permite modificar, actualizar o reemplazar el dataset en tiempo real desde la máquina host sin necesidad de reanudar o reconstruir las imágenes Docker.

---

### E3. Comportamiento de los datos: `docker compose down` vs `docker compose down -v`
* **`docker compose down`:** Detiene y elimina los contenedores y las redes virtuales del proyecto, pero **conserva intactos los volúmenes de datos** almacenados en el host, permitiendo que la información persistida en MySQL se mantenga disponible al volver a levantar los servicios.
* **`docker compose down -v`:** Además de detener contenedores y redes, **elimina permanentemente todos los volúmenes nombrados y anónimos** asociados, destruyendo toda la base de datos MySQL y la información generada.

---

### E4. Rendimiento de MapReduce vs. Script Secuencial en datasets medianos
MapReduce implica un overhead significativo: tiempo de arranque de la máquina virtual de Java (JVM), inicialización del framework MapReduce, serialización de datos y lectura/escritura intermedia en disco durante la fase de *Shuffle & Sort*. 

Para archivos medianos (~400 MB), un script secuencial optimizado en RAM (como Pandas) procesa el archivo en cuestión de segundos, superando a MapReduce al evitar dicho overhead. MapReduce solo es conveniente cuando el tamaño del dataset excede la capacidad de la memoria RAM disponible en una sola máquina o cuando se procesa a través de un clúster distribuido de decenas de nodos.

---

### E5. Diferencia entre CMD / ENTRYPOINT y COPY / ADD
* **`ENTRYPOINT` vs `CMD`:** `ENTRYPOINT` define el comando principal e inmutable que siempre se ejecutará cuando el contenedor inicie, mientras que `CMD` define los argumentos o comandos por defecto que pueden ser sobrescritos fácilmente desde la línea de comandos al ejecutar `docker run`.
* **`ADD` vs `COPY`:** `COPY` solo copia archivos y directorios locales de la máquina host al contenedor. `ADD` incluye esa función y además extrae automáticamente archivos comprimidos (ej. `.tar.gz`) en el destino y permite descargar archivos directamente desde URLs de red.

---

## Parte F. Guía de Preparación para la Defensa Oral

### 1. Cambiar el puerto expuesto de la API
* Editar `docker-compose.yml` en la sección del servicio `api`:
  ```yaml
  ports:
    - "8080:8000"  # Cambia el puerto host de 8000 a 8080