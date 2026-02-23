# SRE Order Tracker — Backend API

FastAPI backend for the E-Commerce Order Tracker demo workload.

## Architecture

```
Frontend (App Service)  →  API Management  →  Backend (AKS)
                                                ├── /api/about
                                                ├── /api/products
                                                ├── /api/orders
                                                ├── /api/inventory
                                                └── /api/health
```

## Local development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

API docs available at http://localhost:8000/api/docs

## API endpoints

| Method | Path                        | Description                |
| ------ | --------------------------- | -------------------------- |
| GET    | /api/about                  | Service info & metadata    |
| GET    | /api/health                 | Service health check       |
| GET    | /api/products               | List products (paginated)  |
| GET    | /api/products/categories    | List categories            |
| GET    | /api/products/{id}          | Get product by ID          |
| GET    | /api/orders                 | List orders (paginated)    |
| GET    | /api/orders/{id}            | Get order by ID            |
| POST   | /api/orders                 | Create a new order         |
| PATCH  | /api/orders/{id}/status     | Update order status        |
| GET    | /api/inventory              | List all inventory         |
| GET    | /api/inventory/{productId}  | Get inventory by product   |

## Docker

```bash
docker build --platform linux/amd64 -t sre-agent-backend .
docker run -p 8000:8000 sre-agent-backend
```

## Kubernetes

```bash
kubectl apply -f k8s/
```

## Environment variables

| Variable                                | Default              | Description                        |
| --------------------------------------- | -------------------- | ---------------------------------- |
| HOST                                    | 0.0.0.0              | Bind address                       |
| PORT                                    | 8000                 | Bind port                          |
| ALLOWED_ORIGINS                         | localhost + app svc  | Comma-separated CORS origins       |
| APPLICATIONINSIGHTS_CONNECTION_STRING   | (empty)              | Azure Monitor connection string    |
| APP_VERSION                             | 1.0.0                | Reported in /api/health            |
| ENVIRONMENT                             | development          | Environment label                  |
| LOG_LEVEL                               | INFO                 | Python logging level               |
