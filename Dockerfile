# Use an official Python runtime as a parent image
ARG PVERSION=3.7
FROM python:${PVERSION}-slim

RUN apt update && apt install -y gcc vim less iputils-ping apt-utils

ENV DHOMEDIR=/app

# Set the working directory to /app
WORKDIR $DHOMEDIR

# Copy the current directory contents into the container at /app
COPY . $DHOMEDIR

# Install any needed packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define environment variable
ENV PYTHONPATH=${PYTHONPATH}:$DHOMEDIR

# Run when the container launches
CMD ["python", "bot_daemon.py" ]
