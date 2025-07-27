FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY tutor_stack_auth/ ./tutor_stack_auth/

# Create keys directory
RUN mkdir -p /keys

EXPOSE 8000

CMD ["uvicorn", "tutor_stack_auth.main:app", "--host", "0.0.0.0", "--port", "8000"] 
