# Lens GPT Backend

A backend for the categorization of clothing pictures using Google Lens and GPT-3.


## Docker

To build the docker image, run the following command:

```bash
docker build -t lens-gpt-backend .
```

To run the docker image, run the following command, replacing `sk-your-key-here` with your OpenAI API key:

```bash
docker run \
    --rm \                      
  -e DISPLAY=:99 \
  -e OPENAI_API_KEY=sk-your-key-here \
  -p 3002:3002  \
  lens-gpt-backend \
  /bin/bash -c "Xvfb :99 -screen 0 1280x1024x24 & poetry run python -m lens_gpt_backend.main"

```


## Architecture

