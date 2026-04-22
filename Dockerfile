# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (leverages Docker layer caching)
COPY requirements.txt .

# Install dependencies (none here, but kept as best practice)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script
COPY password.py .

# Run as non-root user for security
RUN useradd --create-home appuser
USER appuser

# Default command — can be overridden with CLI flags at runtime
ENTRYPOINT ["python", "password.py"]
