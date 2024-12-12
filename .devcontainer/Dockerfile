# Base image for Python development
FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install git and Docker CLI
RUN apt-get update && apt-get install -y \
    git docker.io awscli\
    && rm -rf /var/lib/apt/lists/*

# Set PYTHONPATH
ENV PYTHONPATH=src/

# Copy the source code
COPY . .

