# Flask Api


## Requisitos
- Python 3.8+
- Docker & Docker Compose

## Configuración del entorno de desarrollo

Se recomienda usar un entorno virtual para asegurar compatibilidad con linters, autocompletado y dependencias pero es opcional y no es necesario para levantar y probar la API:

#### Crear entorno virtual
```
python3 -m venv .venv
```

#### Activar entorno virtual
```
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate    # Windows
```

#### Instalar y compilar si se agregan dependencias a requirements.in
```
pip install pip-tools
pip-compile requirements.in
```

#### O solo instalar requirements.txt
```
pip install -r requirements.txt
```

Esto asegura que linters y autocompletado funcionen correctamente dentro del entorno virtual.

## Levantar la Aplicación

#### Añadir las variables de entorno
En .env.template se encuentran las siguientes variables esperadas por la aplicación:
```
MONGO_DB=
MONGO_HOST=
```
las cuales puedes llenar con, por ejemplo, los siguientes datos simples para pruebas, los cuales deben cambiar según el entorno actual (desarrollo, producción):
```
MONGO_DB=people_flow_db
MONGO_HOST=mongodb://mongo:27017/people_flow_db
```
Estas variables deben ir en un archivo nuevo que crees llamado '.env' en la raíz del proyecto

#### Build de docker

Luego de agregar las variables de entorno, levanta la app de docker usando Docker Compose usando el siguiente comando:
```
docker-compose up --build -d
```

> ⚠️ Nota: Si la descarga de imágenes de Docker falla (problema con Docker Hub), la aplicación también se puede ejecutar localmente sin Docker.  
> Para ello, asegúrate de tener instalado requirements.txt y MongoDB corriendo en tu máquina.
> Luego, actualiza la variable de entorno MONGO_HOST en tu archivo .env a:
> ```
> MONGO_HOST=mongodb://localhost:27017/people_flow_db -> 'localhost' en vez de 'mongo'
> ```
> Luego ejecuta la app:
> ```
> flask --app main run --debug --host=0.0.0.0 --port 8000
> ```

#### Semilla Para Poblar la DB
Luego de levantar la app, para poblar la base de datos puedes usar la siguiente ruta:
```
http://localhost:8000/api/v1/seed
```
Esto hará lo siguiente:
- Borrará los datos existentes en las colecciones de Employees y Positions.
- Creará 6 posiciones por defecto.
- Creará 7 empleados asociados a esas posiciones.

Una vez hecho esto, se podrán probar todos los endpoints de Employees y Positions sin necesidad de ingresar datos manualmente.

## Documentación Swagger
```
http://localhost:8000/apidocs
```

## Notas y mejoras futuras

1. El challenge original no requería crear una entidad separada para los puestos, inicialmente, estos se manejaban como un simple string en cada empleado. Sin embargo, esto puede generar inconsistencias: por ejemplo, un mismo puesto podría registrarse como “Software Developer” o “Desarrollador de Software”, lo que dificulta filtrados, reportes y análisis. <br><br>
Para mejorar la consistencia de los datos, decidí crear un modelo independiente Position que almacena cada puesto con un id único en MongoDB.<br><br>
Los beneficios de esta modificación son:

- Filtrado y consultas consistentes: ahora los empleados se relacionan con un position_id en lugar de un string libre, evitando duplicados o variaciones del mismo puesto.

- Integridad de datos: al crear o actualizar empleados, se asegura que siempre se utilice un puesto existente y validado.

- Escalabilidad futura: esta estructura permite agregar atributos adicionales a los puestos (por ejemplo, departamento, nivel o salario base) sin necesidad de modificar directamente los empleados.<br><br>

2. En esta aplicación, cuando se “elimina” un empleado o un puesto, los datos no se borran realmente de la base de datos. En su lugar, se marca al empleado con un campo deleted y se registra la fecha de eliminación en deleted_at. <br><br>
Los motivos principales de este enfoque son:

- Integridad de datos:
Si elimináramos físicamente un empleado que tiene relaciones con otras entidades (por ejemplo, tareas, registros de salarios o proyectos), podrían generarse errores de integridad o inconsistencias en la base de datos.
Manteniendo los registros, aseguramos que todas las referencias sigan siendo válidas.

- Historial y auditoría:
Permite mantener un registro histórico de todos los empleados que han trabajado en la empresa, incluso aquellos que ya no están activos.
Esto facilita auditorías internas, análisis de recursos humanos y seguimiento de cambios a lo largo del tiempo. <br><br>
En la práctica, los endpoints de consulta filtran automáticamente los empleados marcados como deleted=True, mostrando solo los activos, pero la información histórica queda preservada y a futuro podría implementarse otro endpoint para obtener todo el histórico, incluidos los empleados que ya no trabajan más en la empresa por tanto están como eliminados.<br><br>

3. Actualmente, el cálculo de promedio de salarios se realiza on-demand a través del endpoint /salary_average. A futuro, podría agregarse un reporte semanal automático, ejecutado cada lunes, que guarde los promedios para planificación de presupuesto, por ejemplo, guardado en un excel o archivo de texto donde se anote semana a semana la fecha y el promedio de esa semana y asi tener un histórico de promedios a lo largo del año.