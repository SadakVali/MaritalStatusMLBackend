FROM python:3.8

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Update pip and setuptools
RUN pip install --upgrade pip setuptools

# Install necessary dependencies including C++ compilers, CMake, Boost, BLAS, LAPACK, libjpeg, and libpng
RUN apt-get update && \
    apt-get install -y build-essential cmake g++ \
                       libboost-all-dev libblas-dev liblapack-dev \
                       libjpeg-dev libpng-dev

# Install CMake
RUN pip install cmake
RUN pip install dlib

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies within the virtual environment
RUN pip install -r requirements.txt

# Expose the specified port
EXPOSE $PORT

# Command to run the application using Gunicorn
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
