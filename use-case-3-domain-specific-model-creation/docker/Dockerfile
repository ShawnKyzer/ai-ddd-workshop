# Dockerfile (in /home/shawn/projects/ai-ddd-workshop/use-case-3-domain-specific-model-creation/docker/Dockerfile)

FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including SQLite
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the Kedro project directory
COPY ./domain-specific-model-pipeline /app/domain-specific-model-pipeline

# Set the working directory to the Kedro project
WORKDIR /app/domain-specific-model-pipeline

# Install Kedro and project dependencies
RUN pip install --no-cache-dir kedro
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Set up the entry point
CMD ["kedro", "run"]