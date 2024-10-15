from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from typing import List, Tuple, Dict, Any
from datetime import datetime, timedelta
import secrets
import heapq
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class State(BaseModel):
    state: str
    coord: List[float]

estados_grafo = {
    "Alabama": {"Florida": 558, "Georgia": 302, "Mississippi": 222},
    "Alaska": {"Washington": 1800, "Hawaii": 2500},
    "Arizona": {"Utah": 841, "Nevada": 761},
    "Arkansas": {"Mississippi": 322, "Missouri": 302},
    "California": {"Nevada": 521, "Oregon": 668},
    "Colorado": {"New Mexico": 430, "Wyoming": 395},
    "Connecticut": {"New York": 100, "Rhode Island": 119},
    "Delaware": {"Maryland": 73},
    "Florida": {"Alabama": 558, "Georgia": 399},
    "Georgia": {"Alabama": 302, "Florida": 399, "South Carolina": 186, "Tennessee": 379},
    "Hawaii": {"Alaska": 2500},
    "Idaho": {"Montana": 539, "Utah": 429},
    "Illinois": {"Missouri": 314, "Indiana": 268},
    "Indiana": {"Illinois": 268, "Ohio": 194},
    "Iowa": {"Minnesota": 425, "Nebraska": 419},
    "Kansas": {"North Dakota": 747, "Oklahoma": 357},
    "Kentucky": {"West Virginia": 260},
    "Louisiana": {"Mississippi": 247},
    "Maine": {"New Hampshire": 245, "Michigan": 1027},
    "Maryland": {"Virginia": 210, "Delaware": 73},
    "Massachusetts": {"Rhode Island": 76.1, "Vermont": 214},
    "Michigan": {"Maine": 1027, "Wisconsin": 454},
    "Minnesota": {"Wisconsin": 454, "Iowa": 425},
    "Mississippi": {"Alabama": 222, "Louisiana": 247, "Arkansas": 322},
    "Missouri": {"Arkansas": 302, "Illinois": 314},
    "Montana": {"Wyoming": 423, "Idaho": 539},
    "Nebraska": {"Iowa": 419, "South Dakota": 215},
    "Nevada": {"Arizona": 761, "California": 521},
    "New Hampshire": {"Vermont": 151, "Maine": 245},
    "New Jersey": {"Pennsylvania": 243, "New York": 78.6},
    "New Mexico": {"Texas": 498, "Colorado": 430},
    "New York": {"New Jersey": 78.6, "Connecticut": 100},
    "North Carolina": {"South Carolina": 217, "Virginia": 151},
    "North Dakota": {"South Dakota": 346, "Kansas": 747},
    "Ohio": {"Indiana": 194, "Pennsylvania": 409},
    "Oklahoma": {"Kansas": 357, "Texas": 341},
    "Oregon": {"California": 668, "Washington": 457},
    "Pennsylvania": {"Ohio": 409, "New Jersey": 243},
    "Rhode Island": {"Connecticut": 119, "Massachusetts": 76.1},
    "South Carolina": {"Georgia": 186, "North Carolina": 217},
    "South Dakota": {"Nebraska": 215, "North Dakota": 346},
    "Tennessee": {"Georgia": 379},
    "Texas": {"Oklahoma": 341, "New Mexico": 498},
    "Utah": {"Idaho": 429, "Arizona": 841},
    "Vermont": {"Massachusetts": 214, "New Hampshire": 151},
    "Virginia": {"North Carolina": 151, "Maryland": 210, "West Virginia": 255},
    "Washington": {"Oregon": 457, "Alaska": 1800},
    "West Virginia": {"Virginia": 255, "Kentucky": 260},
    "Wisconsin": {"Michigan": 454, "Minnesota": 454},
    "Wyoming": {"Colorado": 395, "Montana": 423}
}


estados = [
    { "state": "Alabama", "coord": [32.806671, -86.791130] },
    { "state": "Alaska", "coord": [61.370716, -152.404419] },
    { "state": "Arizona", "coord": [33.729759, -111.431221] },
    { "state": "Arkansas", "coord": [34.969704, -92.373123] },
    { "state": "California", "coord": [36.116203, -119.681564] },
    { "state": "Colorado", "coord": [39.059811, -105.311104] },
    { "state": "Connecticut", "coord": [41.597782, -72.755371] },
    { "state": "Delaware", "coord": [39.318523, -75.507141] },
    { "state": "Florida", "coord": [27.766279, -81.686783] },
    { "state": "Georgia", "coord": [33.040619, -83.643074] },
    { "state": "Hawaii", "coord": [21.094318, -157.498337] },
    { "state": "Idaho", "coord": [44.240459, -114.478828] },
    { "state": "Illinois", "coord": [40.349457, -88.998996] },
    { "state": "Indiana", "coord": [39.849426, -86.258278] },
    { "state": "Iowa", "coord": [42.011539, -93.210526] },
    { "state": "Kansas", "coord": [39.059811, -98.328000] },
    { "state": "Kentucky", "coord": [37.668140, -84.670067] },
    { "state": "Louisiana", "coord": [31.169546, -91.867805] },
    { "state": "Maine", "coord": [44.693947, -69.381927] },
    { "state": "Maryland", "coord": [39.063946, -76.802101] },
    { "state": "Massachusetts", "coord": [42.230171, -71.531162] },
    { "state": "Michigan", "coord": [43.326618, -84.536095] },
    { "state": "Minnesota", "coord": [45.694454, -93.900192] },
    { "state": "Mississippi", "coord": [32.741646, -89.678696] },
    { "state": "Missouri", "coord": [38.456085, -92.288368] },
    { "state": "Montana", "coord": [46.921925, -110.454353] },
    { "state": "Nebraska", "coord": [41.492537, -99.901810] },
    { "state": "Nevada", "coord": [38.313515, -117.055374] },
    { "state": "New Hampshire", "coord": [43.452492, -71.563896] },
    { "state": "New Jersey", "coord": [40.298904, -74.521011] },
    { "state": "New Mexico", "coord": [34.840515, -106.248482] },
    { "state": "New York", "coord": [42.165726, -74.948051] },
    { "state": "North Carolina", "coord": [35.630066, -79.806419] },
    { "state": "North Dakota", "coord": [47.528912, -99.784012] },
    { "state": "Ohio", "coord": [40.388783, -82.764915] },
    { "state": "Oklahoma", "coord": [35.565342, -96.928917] },
    { "state": "Oregon", "coord": [43.804133, -120.554201] },
    { "state": "Pennsylvania", "coord": [40.590752, -77.209755] },
    { "state": "Rhode Island", "coord": [41.680893, -71.511780] },
    { "state": "South Carolina", "coord": [33.856892, -80.945007] },
    { "state": "South Dakota", "coord": [44.299782, -99.438828] },
    { "state": "Tennessee", "coord": [35.747845, -86.692345] },
    { "state": "Texas", "coord": [31.054487, -97.563461] },
    { "state": "Utah", "coord": [40.150032, -111.862434] },
    { "state": "Vermont", "coord": [44.045876, -72.710686] },
    { "state": "Virginia", "coord": [37.769337, -78.169968] },
    { "state": "Washington", "coord": [47.400902, -121.490494] },
    { "state": "West Virginia", "coord": [38.491226, -80.954201] },
    { "state": "Wisconsin", "coord": [43.784440, -88.787868] },
    { "state": "Wyoming", "coord": [42.755966, -107.302490] }
]



def dijkstra(grafo: Dict[str, Dict[str, int]], inicio: str, destino: str) -> Tuple[int, List[str]]:
    queue = [(0, inicio, [])]
    visitados = set()

    while queue:
        (costo_actual, nodo_actual, camino) = heapq.heappop(queue)

        if nodo_actual in visitados:
            continue

        camino = camino + [nodo_actual]
        visitados.add(nodo_actual)

        if nodo_actual == destino:
            return costo_actual, camino

        for vecino, peso in grafo[nodo_actual].items():
            if vecino not in visitados:
                heapq.heappush(queue, (costo_actual + peso, vecino, camino))

    return float("inf"), []

@app.get("/coordenadas", response_model=List[State])
async def obtener_coordenadas():
    return estados


@app.get("/camino_mas_corto/{inicio}/{destino}")
async def obtener_camino_mas_corto(inicio: str, destino: str) -> Dict[str, Any]:
    if inicio not in estados_grafo or destino not in estados_grafo:
        raise HTTPException(status_code=404, detail="Estado no encontrado")

    distancia, camino = dijkstra(estados_grafo, inicio, destino)
    return {"distancia_total": distancia, "camino": camino}


@app.get("/estados", response_model=List[str])
async def obtener_estados() -> List[str]:
    return list(estados_grafo.keys())




APIKeyHeader_name = "X-API-KEY"
api_key_header = APIKeyHeader(name=APIKeyHeader_name)
api_keys_validas = {}
SUPERUSER_API_KEY = "1236789"  
TIEMPO_EXPIRACION = 60  
SUPERUSER_ROLE = "Benichi"

async def validar_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in api_keys_validas and api_key != SUPERUSER_API_KEY:
        raise HTTPException(status_code=403, detail="Clave API inválida")

    if api_key == SUPERUSER_API_KEY:
        return SUPERUSER_ROLE

    expiracion = api_keys_validas[api_key]
    if datetime.now() > expiracion:
        del api_keys_validas[api_key]  
        raise HTTPException(status_code=403, detail="Clave API ha expirado")


@app.post("/generar-api-key")
def generar_api_key():
    nueva_api_key = secrets.token_hex(32)  
    expiracion = datetime.now() + timedelta(minutes=TIEMPO_EXPIRACION)  
    api_keys_validas[nueva_api_key] = expiracion  
    return {"api_key": nueva_api_key, "expiracion": expiracion.isoformat()}


@app.get("/superuser", dependencies=[Depends(validar_api_key)])
def superuser_endpoint(api_key: str = Depends(api_key_header)):
    if api_key != SUPERUSER_API_KEY:
        raise HTTPException(status_code=403, detail="Acceso denegado: se requiere superusuario")
    return {"detail": "Acceso permitido para el superusuario"}