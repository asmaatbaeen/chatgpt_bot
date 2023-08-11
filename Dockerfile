# docker build -t chatgpt_wimt .
FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y curl build-essential cmake libboost-all-dev git python3.9 && \
    curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -bfp /usr/local && \
    rm -rf /tmp/miniconda.sh && \
    conda update conda && \
    conda install -c conda-forge hnswlib && \
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY app.py app.py
COPY ./materials ./materials

# Set environment variables
ENV APP=app.py
ENV ENV=production
ENV HOST=0.0.0.0
ENV PORT=80

# Expose the specified port
EXPOSE 80

# Start the app
CMD ["python", "app.py"]
