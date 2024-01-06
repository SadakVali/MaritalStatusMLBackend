# Use the latest Miniconda3 base image
FROM continuumio/miniconda3:latest
# Create and activate a virtual environment
RUN conda create --name myenv python=3.8 && \
    echo "conda activate myenv" > ~/.bashrc
ENV PATH="/opt/conda/envs/myenv/bin:$PATH"
SHELL ["/bin/bash", "--login", "-c"]
# Install TensorFlow dependencies
RUN conda install -n myenv -c conda-forge cmake dlib libgcc && \
    conda install -n myenv -c conda-forge tensorflow-cpu && \
    conda clean --all --yes
# Install OpenCV
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
# Copy the application code into the container
COPY . /app
# Set the working directory
WORKDIR /app
# Install Python dependencies within the virtual environment
RUN conda run -n myenv pip install --no-cache-dir -r requirements.txt
# Expose the specified port
EXPOSE $PORT
# Command to run the application using Gunicorn with increased worker memory and different worker class (gevent)
CMD gunicorn --workers=4 --timeout=120 -m=8 --bind 0.0.0.0:$PORT -k gevent --worker-connections=1000 app:app
