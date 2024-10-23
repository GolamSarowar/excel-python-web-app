# Use a slim version of Python for a smaller image size
FROM python:3.10-slim

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 5000

# Command to run the application using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
