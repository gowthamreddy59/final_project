# Running Multilingual T5 in Docker

This project is now configured to run in a Docker container, which provides a consistent, isolated environment with all dependencies properly installed.

## Prerequisites

- Docker Desktop installed on Windows (with WSL 2 backend recommended)
- 8GB+ RAM available
- ~5-10GB free disk space

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Navigate to the project directory
cd multilingual-t5-master

# Build and start the container
docker-compose up -d

# Enter the container shell
docker-compose exec mt5 bash

# Inside container, run Python
python multilingual_t5/evaluation/metrics.py
```

### Option 2: Using Docker Directly

```bash
# Build the image
docker build -t multilingual-t5:latest .

# Run the container
docker run -it --rm \
  -v %cd%:/workspace \
  -p 8888:8888 \
  multilingual-t5:latest bash
```

### Option 3: Using Jupyter Lab (Interactive)

```bash
# Start with Jupyter Lab
docker-compose up

# Access Jupyter at: http://localhost:8888
# Token: mt5password
```

## Running the Project

Once inside the container:

```bash
# Run tests
python -m pytest multilingual_t5/preprocessors_test.py -v
python -m pytest multilingual_t5/tasks_test.py -v
python -m pytest multilingual_t5/evaluation/metrics_test.py -v

# Run Python scripts
python multilingual_t5/utils.py
python multilingual_t5/vocab.py
python multilingual_t5/evaluation/metrics.py
```

## Common Commands

```bash
# Stop the container
docker-compose down

# View container logs
docker-compose logs -f

# Rebuild the image
docker-compose build --no-cache

# Interactive Python shell
docker-compose exec mt5 python
```

## Troubleshooting

- If you get permission errors, ensure Docker daemon is running
- If port 8888 is already in use, modify the port mapping in docker-compose.yml
- For GPU support, ensure NVIDIA Container Runtime is installed

## Project Structure

```
multilingual-t5/
├── multilingual_t5/
│   ├── tasks.py
│   ├── preprocessors.py
│   ├── utils.py
│   ├── vocab.py
│   └── evaluation/
│       └── metrics.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```
