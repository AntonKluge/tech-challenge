# Lens GPT Backend

A backend for the categorization of clothing pictures using Google Lens and GPT-3.




## Docker

To build the docker image, run the following command:

```bash
docker build -t lens-gpt-backend .
```

To run the docker image, run the following command:

```bash
docker run \                      
  --name your_container_name \
  -e DISPLAY=:99 \
  -p 5000:5000  \
  lens-gpt-backend \
  /bin/bash -c "Xvfb :99 -screen 0 1280x1024x24 & poetry run python -m lens_gpt_backend.main"
```


## Architecture

