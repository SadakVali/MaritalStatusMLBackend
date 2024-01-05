# Use the latest Miniconda3 base image
FROM continuumio/miniconda3:latest
# Create and activate a virtual environment
RUN conda create --name myenv python=3.8 && \
    echo "conda activate myenv" > ~/.bashrc
ENV PATH="/opt/conda/envs/myenv/bin:$PATH"
SHELL ["/bin/bash", "--login", "-c"]
# install dependencies, and remove build artifacts
RUN conda install -n myenv -c conda-forge cmake dlib libgcc && \
    conda clean --all --yes
# Set the working directory
WORKDIR /app
# Copy the application code into the container
COPY . /app
# Install Python dependencies within the virtual environment
RUN conda run -n myenv pip install --no-cache-dir -r requirements.txt
# Command to run the application using Gunicorn
# CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:$PORT", "app:app"]
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
