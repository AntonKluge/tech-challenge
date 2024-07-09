# Use an official Python runtime as a parent image, specifically version 3.12
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for general environment and Selenium
RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    x11vnc \
    fluxbox \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set display port and dbus env to avoid chrome crashing
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# Setup the application folder
WORKDIR /app

# Copy the project files into the Docker image
COPY . /app

# Install Poetry
RUN pip install poetry

# Configure Poetry: Disable virtual env creation and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Expose the port Flask is reachable on
EXPOSE 5000

# Set the default command to execute the Flask app using Poetry
CMD ["poetry", "run", "python", "-m", "lens_gpt_backend.main"]
