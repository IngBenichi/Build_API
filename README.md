# FastAPI States and Shortest Paths

This project provides an API to work with a graph of states and calculate the shortest path between them using Dijkstra's algorithm. The API also allows obtaining state coordinates and generating API keys for accessing protected endpoints.

## Requirements

- Python 3.12.3
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IngBenichi/Build_API.git
   cd Build_API
   ```

2. Install the dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

The server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Endpoints

### 1. Get State Coordinates

- **URL**: `/coordinates`
- **Method**: `GET`
- **Description**: Returns a list of states with their coordinates.
- **Response**:
  ```json
  [
    {
      "state": "Alabama",
      "coord": [32.806671, -86.791130]
    },
    ...
  ]
  ```

### 2. Get Shortest Path

- **URL**: `/shortest_path/{start}/{destiny}`
- **Method**: `GET`
- **Description**: Calculates the shortest path between two states.
- **Parameters**:
  - `start`: Name of the starting state.
  - `destiny`: Name of the destination state.
- **Response**:
  ```json
  {
    "total distance": 558,
    "path": ["Alabama", "Florida"]
  }
  ```
- **Errors**:
  - `404`: If the starting or destination state is not found.

### 3. Get List of States

- **URL**: `/states`
- **Method**: `GET`
- **Description**: Returns a list of all state names.
- **Response**:
  ```json
  ["Alabama", "Alaska", "Arizona", ...]
  ```

### 4. Generate API Key

- **URL**: `/generate-api-key`
- **Method**: `POST`
- **Description**: Generates a new API key with an expiration time.
- **Response**:
  ```json
  {
    "api_key": "new_generated_api_key",
    "expiration": "2024-10-15T12:34:56"
  }
  ```

### 5. View Request Log (Superuser Only)

- **URL**: `/superuser`
- **Method**: `GET`
- **Description**: Returns the log of all requests made to the API. Only accessible with the superuser key.
- **Authorization**: Requires the `X-API-KEY` header with the superuser key.

### 6. Projects

- **URL**: `/projects`
- **Method**: `GET`
- **Description**: Retrieves a list of projects.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Project 1",
      "description": "Description of project 1",
      ...
    },
    ...
  ]
  ```

## Usage Examples

### Get State Coordinates

```bash
curl -X GET http://127.0.0.1:8000/coordinates
```

### Get Shortest Path

```bash
curl -X GET http://127.0.0.1:8000/shortest_path/Alabama/Florida
```

### Get List of States

```bash
curl -X GET http://127.0.0.1:8000/states
```

### Generate API Key

```bash
curl -X POST http://127.0.0.1:8000/generate-api-key
```

### View Request Log

```bash
curl -X GET http://127.0.0.1:8000/superuser -H "X-API-KEY: your_superuser_key"
```

### Get List of Projects

```bash
curl -X GET http://127.0.0.1:8000/projects
```

## Testing

To run tests, you can use the `pytest` framework. Make sure you have it installed:

```bash
pip install pytest
```

Then run the tests:

```bash
pytest
```

## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and submit a pull request. Ensure that your code is well-tested and follows the project's coding conventions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---