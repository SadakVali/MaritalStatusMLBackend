FROM continuumio/miniconda3:latest

# Create and activate a virtual environment
RUN conda create --name myenv python=3.8 && \
    echo "conda activate myenv" > ~/.bashrc
ENV PATH="/opt/conda/envs/myenv/bin:$PATH"
SHELL ["/bin/bash", "--login", "-c"]

# Install cmake using pip and dlib using conda
RUN conda run -n myenv pip install cmake && \
    conda install -n myenv -c conda-forge dlib && \
    apt-get remove -y build-essential cmake g++ && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies within the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Expose the specified port
EXPOSE $PORT

# Command to run the application using Gunicorn
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:$PORT", "app:app"]
