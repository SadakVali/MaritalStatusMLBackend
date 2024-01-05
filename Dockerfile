FROM python:3.8
# Update pip and setuptools
RUN pip install --upgrade pip setuptools
# Install necessary dependencies
RUN apt-get update && apt-get install -y cmake build-essential
# Set the working directory
WORKDIR /app
# Copy the application code into the container
COPY . /app
# Install Python dependencies
RUN pip install -r requirements.txt
# Expose the specified port
EXPOSE $PORT
# Command to run the application using Gunicorn
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
