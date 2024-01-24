FROM python:3.9

# Update packages and install curl
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl

# Install Docker
RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Copy requirements.txt and install python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the content of the local src directory to the working directory in the container
COPY ./src /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
