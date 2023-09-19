# FastApi Gateway

FastApi Gateway is a simple gateway for microservices.

It is based on FastApi and uses the same syntax for defining endpoints.
Main purpose of this gateway is to easily define endpoints for microservices in a database and then use them in a gateway.

Currently, it is only possible to define endpoints in a database and use them in a gateway.
In the future, it will be possible to extract endpoints from files and use them in a gateway.

## Installation

```bash
pip install mini-fastapi-gateway
```

## Usage

### Set environment variables

```TEXT
GATEWAY_DB_URL=postgresql://user:password@localhost:5432/db_name
```

### Use GatewayRouter instead of FastApi in your main file

```python
from gateway import GatewayRouter, gateway_crud_router

app = GatewayRouter()

app.include_router(gateway_crud_router)

```

### Make migrations

```bash
fastapi-gateway migrate
```

### Now you can use your dynamic gateway
