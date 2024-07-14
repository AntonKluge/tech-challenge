# Tech Challenge 2024 - ReLoom

## Problem Statement

## Execution

### Docker Compose
The simplest way to run the application is to use `docker-compose`. This will start the frontend and backend services in separate containers.

**Requirements:**
- Docker

```bash
docker-compose up
```

The frontend will be available at `http://localhost:3001` and the backend will be available at `http://localhost:3002`.

### Manual Setup
If you prefer to run the frontend and backend services manually, you can follow the instructions below.

**Requirements:**
- Node.js
- Yarn
- Python 3.8
- Poetry

#### Frontend
```bash
cd frontend
yarn install
yarn dev
```

#### Backend
```bash
cd backend
poetry install
poetry run python -m lens_gpt_backend.main
```

## Technical Background

### Frontend
Read the [frontend documentation](docs/frontend.md) for more information.

### Backend
Read the [backend documentation](docs/backend.md) for more information.