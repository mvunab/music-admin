# Utilidades para Desarrollo y Pruebas

Este directorio contiene scripts y utilidades para facilitar el desarrollo, pruebas y mantenimiento de la aplicación.

## Scripts Disponibles

### Utilidades de Base de Datos

- **`db_utils.py`**: Funciones auxiliares para conectar y ejecutar consultas en la base de datos MySQL.
  
- **`fix_database.py`**: Script para corregir la estructura de la base de datos, añadiendo columnas faltantes como `rol_plataforma` e `integrante_id`.
  
- **`enum_checker.py`**: Verifica la compatibilidad entre los valores de enum definidos en el código (RolUsuario) y los valores almacenados en la base de datos.

### Utilidades de Desarrollo

- **`setup_dev.py`**: Script para configurar el entorno de desarrollo. Ejecuta automáticamente los scripts de verificación y corrección, y opcionalmente inicia la aplicación.

### Utilidades de Prueba

- **`test_api.py`**: Realiza pruebas básicas de los principales endpoints de la API para verificar que estén funcionando correctamente.

## Uso

Los scripts pueden ejecutarse directamente desde la línea de comandos:

```bash
# Verifica la estructura de la base de datos y aplica correcciones si es necesario
python backend/utils/fix_database.py

# Verifica la compatibilidad de los valores de enum
python backend/utils/enum_checker.py

# Configura el entorno de desarrollo y opcionalmente inicia la aplicación
python backend/utils/setup_dev.py

# Realiza pruebas básicas de la API
python backend/utils/test_api.py
```

También se pueden importar y utilizar las funciones definidas en estos scripts desde otros módulos Python.
