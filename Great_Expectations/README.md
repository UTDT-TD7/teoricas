# Calidad de Datos

## Descripción

Ejemplo para la clase de Calidad y Gobernanza de Datos. El ejemplo muestra el uso de la herramienta Great Expectations para monitorear un pequeño pipeline de procesamiento.

Un programa en Python extrae diariamente las cotizaciones de acciones de la API de polygon.io, y las guarda en una base de datos PostgreSQL.

Con Great Expectations controlamos que:
    - Los datos en PostgreSQL se mantengan actualizados.
    - No aparezcan valores nulos en las cotizaciones.

Para simular fallas, intentamos:
    - Modificar el nombre de una columna traída desde la API de polygon.io (ocurre un error y no se inserta)
    - Poner un valor nulo en la columna de cotización de un día
    
## Uso

docker compose build
docker compose up
