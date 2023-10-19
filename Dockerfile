# Use the official Python image from the DockerHub
FROM python:3.11

# Set the working directory in docker
WORKDIR /app

# Install essential build tools required for compiling some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Set Streamlit's configuration settings
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run Streamlit app
ENTRYPOINT [ "streamlit", "run", "streamlit_app.py" ]
