FROM python:3.11-slim

LABEL maintainer="SALENE Team"
LABEL description="SALENE Neural Consciousness Agent"

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libsndfile1 \
    libportaudio2 \
    libportaudiocpp0 \
    libasound2-dev \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy SALENE code
COPY . /app/salene/

# Setup environment
ENV PYTHONPATH="/app/salene:/app/hermes-agent"
ENV SALENE_HOME="/app/.hermes/salene"
ENV HERMES_HOME="/app/.hermes"

# Create directories
RUN mkdir -p /app/.hermes/agents \
    /app/.hermes/sanctuary_memories \
    /app/.hermes/skins \
    /app/.hermes/logs

# Copy default configs
COPY config/docker-config.yaml /app/.hermes/config.yaml
COPY config/docker-salene.yaml /app/.hermes/salene/config.yaml

# Create non-root user
RUN useradd -m -u 1000 salene && \
    chown -R salene:salene /app

USER salene

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.path.insert(0, '/app/salene'); from free_energy_agent.core import FreeEnergyAgent; print('OK')" || exit 1

# Expose ports
EXPOSE 8080

# Default command
CMD ["python3", "/app/salene/salene_daemon.py"]
