# Music Admin - Docker

Este repositorio contiene una aplicación para la gestión de bandas musicales, configurada para ejecutarse en contenedores Docker.

## Requisitos

- Docker
- Docker Compose

## Instrucciones de uso

Se incluye un script avanzado (`docker.sh`) para gestionar los contenedores Docker con verificaciones y mensajes verbosos:

```bash
# Iniciar la aplicación (con verificación de servicios)
./docker.sh up

# Detener la aplicación
./docker.sh down

# Ver los logs de todos los servicios
./docker.sh logs

# Ver los logs de un servicio específico
./docker.sh logs mysql
./docker.sh logs backend
./docker.sh logs frontend
./docker.sh logs mongodb

# Reiniciar los contenedores
./docker.sh restart

# Construir los contenedores (útil después de cambios en el código)
./docker.sh build

# Verificar el estado de los contenedores
./docker.sh status

# Verificar la conectividad entre servicios
./docker.sh check

# Limpiar recursos Docker no utilizados
./docker.sh clean

# Listar contenedores en ejecución
./docker.sh ps

# Abrir una terminal bash en un contenedor
./docker.sh bash backend
./docker.sh bash frontend
```

> **Nota:** El script ya incluye `sudo` en los comandos para usuarios que lo requieran.

## Acceso a la aplicación

- **Frontend:** http://localhost
- **API Backend:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs

## Puertos utilizados

- **80**: Frontend (Nginx)
- **8000**: Backend (FastAPI)
- **3306**: MySQL
- **27017**: MongoDB

## Estructura de archivos Docker

- `docker-compose.yml`: Configuración de servicios con healthchecks
- `Dockerfile.backend`: Imagen para el backend con Python/FastAPI
- `Dockerfile.frontend`: Imagen para el frontend con Node.js/Vue
- `docker/nginx.conf`: Configuración del servidor web Nginx
- `docker.sh`: Script avanzado para gestionar los contenedores

## Características de la configuración Docker

- **Healthchecks**: Todos los servicios principales tienen configurados healthchecks para garantizar su correcto funcionamiento
- **Dependencias entre servicios**: El backend espera a que las bases de datos estén listas antes de iniciar
- **Redes aisladas**: Los servicios se comunican a través de una red Docker dedicada
- **Volúmenes persistentes**: Los datos de las bases de datos se almacenan en volúmenes Docker
- **Variables de entorno**: Configuración centralizada mediante el archivo `.env`
- **Verificación de servicios**: El script `docker.sh` verifica la correcta ejecución de todos los componentes
