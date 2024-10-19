from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from typing import List, Tuple, Dict, Any
from datetime import datetime, timedelta
import secrets
import heapq
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional

app = FastAPI()


request_log: List[Dict] = []

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

states_graph = {
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


states = [
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



def dijkstra(graph: Dict[str, Dict[str, int]], start: str, destiny: str) -> Tuple[int, List[str]]:
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (current_cost, current_node, path) = heapq.heappop(queue)

        if current_node in visited:
            continue

        path = path + [current_node]
        visited.add(current_node)

        if current_node == destiny:
            return current_cost, path

        for neighbor, weight in graph[current_node].items():
            if neighbor not in visited:
                heapq.heappush(queue, (current_cost + weight, neighbor, path))

    return float("inf"), []

@app.get("/coordinates", response_model=List[State])
async def get_coordinates():
    return states


@app.get("/shortest_path/{start}/{destiny}")
async def get_shortest_path(start: str, destiny: str) -> Dict[str, Any]:
    if start not in states_graph or destiny not in states_graph:
        raise HTTPException(status_code=404, detail="Status not found")

    distance, path = dijkstra(states_graph, start, destiny)
    return {"total distance": distance, "path": path}


@app.get("/states", response_model=List[str])
async def get_states() -> List[str]:
    return list(states_graph.keys())


APIKeyHeader_name = "X-API-KEY"
api_key_header = APIKeyHeader(name=APIKeyHeader_name)
valid_api_keys = {}
SUPERUSER_API_KEY = "1236789"  
EXPIRATION_TIME = 60  
SUPERUSER_ROLE = "Benichi"

async def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in valid_api_keys and api_key != SUPERUSER_API_KEY:
        raise HTTPException(status_code=403, detail="API key has expired")

    if api_key == SUPERUSER_API_KEY:
        return SUPERUSER_ROLE

    expiration = valid_api_keys[api_key]
    if datetime.now() > expiration:
        del valid_api_keys[api_key]  
        raise HTTPException(status_code=403, detail="Clave API ha expirado")


@app.post("/generate-api-key")
def generate_api_key():
    new_api_key = secrets.token_hex(32)  
    expiration = datetime.now() + timedelta(minutes=EXPIRATION_TIME)  
    valid_api_keys[new_api_key] = expiration  
    return {"api_key": new_api_key, "expiration": expiration.isoformat()}


@app.get("/superuser", dependencies=[Depends(validate_api_key)])
def superuser_endpoint(api_key: str = Depends(api_key_header)):
    if api_key != SUPERUSER_API_KEY:
        raise HTTPException(status_code=403, detail="Access denied: superuser required")
    return {"detail": "Access allowed for superuser"}


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI"}

app.mount("/src/assets/Stadistics", StaticFiles(directory="static"), name="static")

# Datos de ejemplo
statistics = [
    {
        "id": 1,
        "name": "Today's Money",
        "price": 53000,
        "increase": 55,
        "image": "./src/assets/Stadistics/wallet.svg"  
    },
    {
        "id": 2,
        "name": "Today's Users",
        "price": 2300,
        "increase": 5,
        "image": "./src/assets/Stadistics/land.svg"
    },
    {
        "id": 3,
        "name": "New Clients",
        "price": 3052,
        "increase": -14,
        "image": "./src/assets/Stadistics/document.svg"
    },
    {
        "id": 4,
        "name": "Total Sales",
        "price": 173000,
        "increase": 8,
        "image": "./src/assets/Stadistics/car.svg"
    },
]


@app.get("/statistics")
def get_data():
    return JSONResponse(content=statistics)


class Order(BaseModel):
    design_changes: Optional[int] = None
    title: Optional[str] = None
    date: str
    image: Optional[str] = None


class MonthlyEarnings(BaseModel):
    percentage: str
    image: str


class OrdersOverview(BaseModel):
    monthly_earnings: MonthlyEarnings
    orders: List[Order]


orders_overview = OrdersOverview(
    monthly_earnings=MonthlyEarnings(
        percentage="30%",
        image="./src/assets/Stadistics/check.svg" 
    ),
    orders=[
        {
            "id": 1,
            "design_changes": 2400,
            "date": "22 DEC 7:20 PM",
            "image": "./src/assets/Stadistics/campaign.svg"
        },
        {
            "id": 2,
            "title": "New order #4219423",
            "date": "21 DEC 11:21 PM",
            "image": "./src/assets/Stadistics/html.svg" 
        },
        {
            "id": 3,
            "title": "Server Payments for April",
            "date": "21 DEC 09:28 PM",
            "image": "./src/assets/Stadistics/car2.svg" 
        },
        {
            "id": 4,
            "title": "New card added for order #3210145",
            "date": "20 DEC 03:52 PM",
            "image": "./src/assets/Stadistics/card.svg" 
        },
        {
            "id": 5,
            "title": "Unlock packages for Development",
            "date": "19 DEC 11:35 PM",
            "image": "./src/assets/Stadistics/unlocked.svg"
        },
        {
            "id": 6,
            "title": "New order #9851258",
            "date": "18 DEC 04:41 PM",
            "image": "./src/assets/Stadistics/xd.svg"  
        }
    ]
)



@app.get("/orders")
def get_orders():
    return JSONResponse(content=orders_overview.dict())

app.mount("/src/assets/Projects", StaticFiles(directory="projects"), name="projects")
class Projects(BaseModel):
    id: int
    name: Optional[str] = None
    img: Optional[str] = None
    members: Optional[str] = None
    budget: Optional[int] = 0
    completion: Optional[int] = None

class MonthlyEarning(BaseModel):
    percentage: str
    image: str


class ProjectsOverview(BaseModel):
    monthly_earning: MonthlyEarning
    projects: List[Projects]

projects_overview = ProjectsOverview(
    monthly_earning=MonthlyEarning(
        percentage="30",
        image="./src/assets/Stadistics/check.svg" 
    ),
projects = [
    {
      "id" : 1,
      "name": "Chakra Soft UI Version",
      "img": "./src/assets/Stadistics/xd.svg",
      "members": "./src/assets/Projects/avatarsthree.svg",
      "budget": 14000,
      "completion": 60
    },
    {
      "id" : 2,
      "name": "Add Progress Track",
      "img": "./src/assets/Projects/addprogress.svg",
      "members": "./src/assets/Projects/avatartwo.svg",
      "budget": 3000,
      "completion": 10
    },
    {
      "id" : 3,
      "name": "Fix Platform Errors",
      "img": "./src/assets/Projects/fixplatform.svg",
      "members": "./src/assets/Projects/avatartwo.svg",
      "budget": 0,
      "completion": 100
    },
    {
      "id" : 4,
      "name": "Launch our Mobile App",
      "img": "./src/assets/Projects/launchmobile.svg",
      "members": "./src/assets/Projects/avatarfour.svg",
      "budget": 32000,
      "completion": 100
    },
    {
      "id" : 5,
      "name": "Add the New Pricing Page",
      "img": "./src/assets/Projects/addpricing.svg",
      "members": "./src/assets/Projects/avatarsthree.svg",
      "budget": 400,
      "completion": 25
    },
    {
      "id" : 6,
      "name": "Redesign New Online Shop",
      "img": "./src/assets/Projects//redesign.svg",
      "members": "./src/assets/Projects/avatartwo.svg",
      "budget": 7600,
      "completion": 40
    },
]
)

@app.get("/projects")
def get_data():
    return JSONResponse(content=projects_overview.dict())

