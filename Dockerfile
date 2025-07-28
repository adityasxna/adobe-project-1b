# Dockerfile for Round 1B

# Use the same base image for consistency
FROM --platform=linux/amd64 python:3.9-slim-buster

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Key Difference for Part 1B ---
# Copy the pre-downloaded models into the image.
# This makes the model available offline inside the container.
COPY ./models/ /app/models/

# Copy the application code
COPY ./app/ .

# Run the main script for Round 1B
CMD ["python", "main.py"]