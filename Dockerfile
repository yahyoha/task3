FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install Java
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

COPY ./ /app/

RUN pip install -r /app/requirements.txt

CMD ["python", "cloudbillingtool-run.py", "--hetzner_data", "/data/hetzner/*.csv", "--azure_data", "/data/azure/*.csv", "--aws_data", "", "--metadata", "/metadata", "--output_path", "/output/" ]