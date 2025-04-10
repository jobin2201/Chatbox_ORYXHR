# Use the official Python image as the base image
FROM python:3.11.11

# Set the working directory inside the container
WORKDIR /app

# Copy all necessary files into the container
COPY app_new11.py .
COPY requirements.txt .
COPY predefined_response.json .
COPY .env .

# Install dependencies
RUN pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app_new11.py"]
