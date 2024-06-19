
# Movies Management gRPC Service

This project implements a gRPC service for managing movies and actors, featuring JWT authentication and distributed tracing.

## Features
- **Add Movie**: Add a new movie.
- **Get Movie**: Retrieve movie details.
- **Get Actor**: Retrieve actor details.
- **Change Rating**: Update movie rating.
- **Get Movies by Director**: Stream movies by director.
- **JWT Authentication**: Secure endpoints with JWT tokens.
- **Distributed Tracing**: Track requests with trace IDs.

## Setup

### Prerequisites
- Python 3.7+
- `grpcio` and `grpcio-tools`
- `pyjwt`

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/naveenpiedy/gRPCDemo.git
    cd movies-management-grpc
    ```

2. Install dependencies:
    ```sh
    pip install grpcio grpcio-tools pyjwt
    ```

3. Generate gRPC code from the `.proto` file:
    ```sh
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. movies_management.proto
    ```

## Usage

### Running the Server
```sh
python server.py
```

### Running the Client
```sh
python client.py
```

### Example Client Methods

- **Get Movie**:
    ```python
    get_movies('Avengers')
    ```

- **Get Actor**:
    ```python
    get_actors('Robert Downey Jr.')
    ```

- **Add Movie**:
    ```python
    add_movie('4', 'Minnale', ['Madhavan', 'Reema Sen'], 'Gautham Vasudev Menon', 4.5)
    ```

- **Change Rating**:
    ```python
    change_rating('Minnale', 5.0)
    ```

- **Get Movies by Director**:
    ```python
    get_movie_by_director('Joss Whedon')
    ```

## Error Handling

Custom errors are handled using the `errors.py` module:
- **CustomError**: Base class for custom errors.
- **NotFoundError**: Raised when a resource is not found.
- **UnauthorizedError**: Raised when access is unauthorized.
- **InternalServerError**: Raised for internal server errors.

## Authentication and Tracing

- **JWT Authentication**: Managed by `jwt_utils.py`.
- **Distributed Tracing**: Each request includes a trace ID.

## Interceptors

A logging interceptor is implemented to log request details.

Screenshot of Server Side logging
![image](https://github.com/naveenpiedy/gRPCDemo/assets/5013693/be6cf5ad-826b-4e94-99c6-2b9d639d009c)

