# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install curl for Poetry installation
RUN apt-get update && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using the official installation script
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure poetry is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock /app/

# Install the dependencies, updating the lock file if necessary
RUN poetry config virtualenvs.create false \
    && poetry lock --no-update \
    && poetry install --only main

# Copy the rest of the application code to the container
COPY . /app/sixdegrees

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "sixdegrees.server:app", "--host", "0.0.0.0", "--port", "8000"]
