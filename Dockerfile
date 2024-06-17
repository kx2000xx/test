# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY bot.py .
COPY restriction.py .
COPY settings.py .

# Set the command to run your script
CMD ["python", "bot.py"]
