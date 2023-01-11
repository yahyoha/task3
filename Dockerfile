FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install Java
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

COPY ./ /app/

RUN pip install -r /app/requirements.txt

CMD ["python", "spark-run-cloudbillingtool.py", "/data/hetzner/*.csv", "/data/azure/*.csv", "/metadata", "/output/" ]