# Use an official Python runtime as a parent image
FROM python:3.10-slim

ARG TOKEN_BOT
ENV TOKEN_BOT=$TOKEN_BOT

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV TZ=America/Argentina/Buenos_Aires
# Run your Python application
CMD ["python", "app.py"]