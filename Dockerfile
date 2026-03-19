# Base repository based on Python 3.10
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies for Pillow and sqlite
RUN apt-get update \
    && apt-get install -y gcc zlib1g-dev libjpeg-dev sqlite3 \
    && apt-get clean

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "alkinvaran_proj.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
