Claro, aquí tienes el texto sin formato Markdown:

---

# FastAPI Estados y Caminos Más Cortos

Este proyecto proporciona una API para trabajar con un grafo de estados y calcular el camino más corto entre ellos utilizando el algoritmo de Dijkstra. La API también permite obtener coordenadas de estados y generar claves de API para acceder a los endpoints protegidos.

## Requisitos

- Python 3.12.3
- FastAPI
- Uvicorn

## Instalación

1. Clona el repositorio:
   git clone https://github.com/IngBenichi/Build_API.git
   cd Build_API

2. Instala las dependencias:
   pip install fastapi uvicorn

3. Ejecuta el servidor:
   uvicorn main:app --reload

El servidor se iniciará en http://127.0.0.1:8000.

## Endpoints

### 1. Obtener Coordenadas de los Estados

- **URL**: /coordenadas
- **Método**: GET
- **Descripción**: Devuelve una lista de estados con sus coordenadas.
- **Respuesta**:
  [
    {
      "state": "Alabama",
      "coord": [32.806671, -86.791130]
    },
    ...
  ]

### 2. Obtener el Camino Más Corto

- **URL**: /camino_mas_corto/{inicio}/{destino}
- **Método**: GET
- **Descripción**: Calcula el camino más corto entre dos estados.
- **Parámetros**:
  - inicio: Nombre del estado de origen.
  - destino: Nombre del estado de destino.
- **Respuesta**:
  {
    "distancia_total": 558,
    "camino": ["Alabama", "Florida"]
  }
- **Errores**:
  - 404: Si el estado de inicio o destino no se encuentra.

### 3. Obtener Lista de Estados

- **URL**: /estados
- **Método**: GET
- **Descripción**: Devuelve la lista de nombres de todos los estados.
- **Respuesta**:
  ["Alabama", "Alaska", "Arizona", ...]

### 4. Generar Clave API

- **URL**: /generar-api-key
- **Método**: POST
- **Descripción**: Genera una nueva clave API con un tiempo de expiración.
- **Respuesta**:
  {
    "api_key": "nueva_api_key_generada",
    "expiracion": "2024-10-15T12:34:56"
  }

### 5. Ver Registro de Peticiones (Solo Superusuario)

- **URL**: /registro
- **Método**: GET
- **Descripción**: Devuelve el registro de todas las peticiones realizadas a la API. Solo accesible con la clave de superusuario.
- **Autorización**: Requiere la cabecera X-API-KEY con la clave de superusuario.
- **Respuesta**:
  [
    {
      "timestamp": "2024-10-15T12:34:56",
      "ruta": "/coordenadas",
      "cliente": "127.0.0.1",
      "rol": "Benichi"
    },
    ...
  ]

## Seguridad

El acceso a algunos endpoints está protegido mediante claves de API. La clave de superusuario es 1236789 y tiene acceso ilimitado. Las claves generadas tienen un tiempo de expiración definido.

## CORS

La API permite solicitudes desde cualquier origen configurando allow_origins=["*"].

## Algoritmo de Dijkstra

El algoritmo implementado en la función dijkstra() calcula el camino más corto en un grafo no dirigido, representado como un diccionario de adyacencia.

## Contribuciones

Si deseas contribuir, por favor abre un pull request o crea un issue para discutir los cambios.

## Licencia

Este proyecto está bajo la Licencia MIT.

--- 
