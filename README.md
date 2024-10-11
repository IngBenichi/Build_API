# API de Estados y Distancias con FastAPI

Esta API permite obtener información sobre estados de EE. UU., sus distancias entre sí, y calcular la ruta más corta entre dos estados utilizando el algoritmo de Dijkstra. Además, incluye autenticación basada en claves API y un rol de superusuario.

## Contenidos

- [Instalación](#instalación)
- [Endpoints](#endpoints)
  - [GET /coordenadas](#get-coordenadas)
  - [GET /camino_mas_corto/{inicio}/{destino}](#get-camino_mas_corto)
  - [GET /estados](#get-estados)
  - [POST /generar-api-key](#post-generar-api-key)
  - [GET /superuser](#get-superuser)
- [Autenticación](#autenticación)
- [Algoritmo de Dijkstra](#algoritmo-de-dijkstra)

---

## Instalación

1. Clona el repositorio o descarga los archivos.
2. Instala las dependencias requeridas:

    ```bash
    pip install fastapi uvicorn
    ```

3. Ejecuta la aplicación:

    ```bash
    uvicorn main:app --reload
    ```

## Endpoints

### GET /coordenadas

Este endpoint devuelve las coordenadas geográficas (latitud y longitud) de cada estado.

#### Ejemplo de respuesta:

```json
{
  "Alabama": [32.806671, -86.791130],
  "Alaska": [61.370716, -152.404419],
  "Arizona": [33.729759, -111.431221],
  ...
}
