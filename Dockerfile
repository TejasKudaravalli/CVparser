# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv properly
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH manually
ENV PATH="/root/.local/bin:$PATH"

# Clone the GitHub repository
RUN git clone https://github.com/TejasKudaravalli/CVparser.git .

# Install Python dependencies with uv
RUN uv pip install --system .

# Download spaCy models
RUN python -m spacy download en_core_web_sm \
    && python -m spacy download en_core_web_md

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
