# Password Generator Command Line App

A secure command-line password generator written in Python and packaged as a Docker container.
Passwords are generated using Python's `secrets` module, which draws from the OS entropy pool
(`/dev/urandom`) — making them cryptographically secure and suitable for real-world use.

***

## Project Structure

```
password-generator/
├── password.py        # Main application script
├── requirements.txt   # Dependencies (stdlib only — empty)
├── Dockerfile         # Docker image definition
└── README.md          # This file
```

***

## Requirements

- Python 3.12+ (for local use)
- Docker (for containerized use)

***

## Running Locally

```bash
python password.py
python password.py --length 24
python password.py --count 5 --length 16 --no-symbols
python password.py --help
```

***

## CLI Options

| Flag            | Default | Description                                      |
|-----------------|---------|--------------------------------------------------|
| `--length`, `-l`  | `16`    | Length of the generated password                 |
| `--count`, `-c`   | `1`     | Number of passwords to generate                  |
| `--no-upper`    | off     | Exclude uppercase letters (A–Z)                  |
| `--no-lower`    | off     | Exclude lowercase letters (a–z)                  |
| `--no-digits`   | off     | Exclude digits (0–9)                             |
| `--no-symbols`  | off     | Exclude symbols (`!@#$...`)                      |
| `--exclude`, `-e` | `""`    | Exclude specific characters (e.g. `"O0lI1"`)    |

***

## Docker Usage

### Pull from Docker Hub

```bash
docker pull maksimciz/password-generator:1.0
```

### Build Locally

```bash
docker build -t password-generator:1.0 .
```

### Run

```bash
# Default — 16-character password
docker run password-generator:1.0

# Custom length
docker run password-generator:1.0 --length 24

# No symbols, 20 characters
docker run password-generator:1.0 --length 20 --no-symbols

# Generate 5 passwords
docker run password-generator:1.0 --count 5 --length 12

# Exclude lookalike characters
docker run password-generator:1.0 --length 16 --exclude "O0lI1"

# Show help
docker run password-generator:1.0 --help
```

***

## Dockerfile Overview

```dockerfile
FROM python:3.12-slim        # Minimal official Python base image
WORKDIR /app                 # Set working directory
COPY requirements.txt .      # Copy dependencies first
RUN pip install --no-cache-dir -r requirements.txt
COPY password.py .           # Copy application script
RUN useradd --create-home appuser
USER appuser                 # Run as non-root user for security
ENTRYPOINT ["python", "password.py"]
```

***

## Security Notes

- Uses Python's `secrets` module (not `random`) — backed by the OS entropy pool (`/dev/urandom`)
- No external dependencies — zero third-party attack surface
- Container runs as a non-root user

***

## Docker Hub

Image available at:
```
docker pull maksimciz/password-generator:1.0
```
