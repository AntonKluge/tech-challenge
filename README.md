# Tech Challenge 2024 - ReLoom

## Problem Statement

This application is a prototype for a tool that helps companies in the resale market to identify and price second
hand clothing items. As correctly identifying and pricing items is a time-consuming process which often includes human
labor, the tool aims to automate this process using image recognition and natural language processing. The tool should
be able to categorize clothing items based on images and provide a price estimate for the item based of available second
hand market data.

## Execution

### Docker Compose

The simplest way to run the application is to use `docker-compose`. This will start the frontend and backend
services in separate containers. For the application to work correctly, you need to set the `OPENAI_API_KEY`
environment variable to your OpenAI API key. It only requires Docker to be installed on your system. Run
the following commands to start the application in the root directory of the project:

```bash
export OPENAI_API_KEY=sk-your-key-here
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