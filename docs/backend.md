# Backend

The backend, which is responsible for the identification based of a picture and streaming that information to the 
frontend is build in Python 3.12 using poetry as its dependency manager. The backend is a flask application that
utilizes the Google Lens features by utilizing Selenium to access the Google Lens website and GPT-4o to generate
a description of the picture. The backend is containerized using Docker and can be run using the following command:


## Usage 

The usage of the backend in production requires Docker to be installed.

```bash
cd lens-gpt-backend
docker build -t lens-gpt-backend .
docker run \
    --rm \                      
  -e DISPLAY=:99 \
  -p 3002:5000  \
  lens-gpt-backend \
  /bin/bash -c "Xvfb :99 -screen 0 1280x1024x24 & poetry run python -m lens_gpt_backend.main"
```

The application can then be accessed at `http://localhost:3002` via curl or a web browser. The backend comes with a 
demo frontend which allows the user to upload a picture and display the raw information that are streamed back 
from the backend. The classification can be accessed via the `/classify` endpoint and the frontend can be 
accessed via the `/` endpoint. If the backend should be used just over the API, the following curl command 
can be used, if the current directory contains an ``img.png``

```bash 
curl --no-buffer -X POST -F "file=@img.png" http://localhost:3002
```

#### 4. Set Up the Project

Navigate to the `lens-gpt-backend` directory and install the project dependencies:

```bash
cd path/to/lens-gpt-backend
poetry install
```

#### 5. Run the Server

Once all the requirements are met, run the server using the command:

```bash
poetry run python -m lens_gpt_backend.main
```

This command starts the server, allowing you to begin development.

