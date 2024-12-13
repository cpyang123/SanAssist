# Use the official Python image from the Docker Hub
FROM python:3.10-slim


# Install git and docker.io, then clean up the apt cache
RUN apt-get update && apt-get install -y \
    git docker.io \
    && rm -rf /var/lib/apt/lists/*


ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY


# Set the working directory in the container
WORKDIR /app

# COPY . /app 
# # Copy specific directories
COPY assets /app/assets
COPY data /app/data
COPY models /app/models
COPY pyconfigs /app/pyconfigs
COPY seeds /app/seeds
COPY src /app/src
COPY dashboards /app/dashboards


# Copy specific files
COPY smaller_inference_LLM_model.py /app/smaller_inference_LLM_model.py
COPY Dockerfile /app/Dockerfile
COPY env.yml /app/env.yml
COPY inference_LLM_model.py /app/inference_LLM_model.py
COPY Makefile /app/Makefile
COPY requirements.txt /app/requirements.txt
COPY squirrels.yml /app/squirrels.yml


# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 4465 for external access
EXPOSE 4465

# Define the command to run the application
CMD ["squirrels", "run", "--host=0.0.0.0", "--port=4465"]
