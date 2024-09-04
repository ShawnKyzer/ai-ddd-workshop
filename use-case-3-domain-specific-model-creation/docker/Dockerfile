FROM nvidia/cuda:11.8.0-devel-ubuntu22.04
RUN apt-get update && apt-get install -y python3 python3-pip

# Set CUDA_HOME environment variable
ENV CUDA_HOME /usr/local/cuda
ENV PATH ${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH ${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

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
RUN pip install torch torchvision torchaudio
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Set up the entry point
CMD ["kedro", "run"]