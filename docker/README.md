# Music Admin - Entorno Dockerizado

Este documento describe cómo ejecutar la aplicación Music Admin en un entorno containerizado utilizando Docker.

## Requisitos previos

- Docker
- Docker Compose (incluido en Docker Desktop para Windows/Mac)

## Estructura de contenedores

La aplicación está dividida en los siguientes contenedores:

1. **MySQL**: Base de datos principal
2. **MongoDB**: Base de datos para almacenamiento de canciones (opcional)
3. **Backend**: API FastAPI
4. **Frontend**: Aplicación Vue.js servida por Nginx

## Configuración

Todas las variables de entorno están definidas en el archivo `.env` en la raíz del proyecto. Si no existe, se creará automáticamente con valores predeterminados al ejecutar el script `docker-start.sh`.

### Variables principales:

```
# MySQL
MYSQL_ROOT_PASSWORD=Mati10.-
MYSQL_DATABASE=music_admin
MYSQL_USER=admin
MYSQL_PASSWORD=password

# MongoDB
MONGO_USER=admin
MONGO_PASSWORD=password
MONGO_DATABASE=music_admin

# JWT (Backend)
SECRET_KEY=tu_clave_secreta_muy_segura_para_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Ejecución

### Usando el script de inicio

```bash
# Modo de desarrollo (logs en consola)
./docker-start.sh dev

# Modo producción (en segundo plano)
./docker-start.sh detach

# Reconstruir contenedores
./docker-start.sh build

# Detener todos los contenedores
./docker-start.sh down

# Ver logs
./docker-start.sh logs
```

### Usando Docker Compose directamente

```bash
# Iniciar todos los servicios
docker-compose up

# Iniciar en segundo plano
docker-compose up -d

# Reconstruir contenedores
docker-compose up --build

# Detener todos los servicios
docker-compose down
```

## Solución de problemas

### Problemas de permisos con Docker Buildx

Si encuentras un error como este:

```
Compose can now delegate builds to bake for better performance.
To do so, set COMPOSE_BAKE=true.
stat /Users/username/.docker/buildx/instances: permission denied
```

Puedes resolverlo de varias maneras:

1. **Reiniciar Docker**: Usa el script de reinicio incluido:
   ```bash
   ./docker/restart-docker.sh
   ```

2. **Usar el script alternativo**: Que desactiva Buildx:
   ```bash
   ./docker/docker-compose-simple.sh up
   ```

3. **Ejecutar con las variables de entorno adecuadas**:
   ```bash
   DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 docker-compose up
   ```

### Otros problemas comunes

Si encuentras otros problemas con los contenedores, puedes verificar los logs:

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql
docker-compose logs mongodb
```

Para reiniciar un servicio específico:

```bash
docker-compose restart backend
```
