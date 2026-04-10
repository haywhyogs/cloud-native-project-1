# Use official Python image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy dependencies first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port your Flask app runs on
EXPOSE 80

# Run the app
CMD ["python", "app.py"]