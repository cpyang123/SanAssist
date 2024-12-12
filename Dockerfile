# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install git and ensure it is in the PATH
RUN apt-get update && apt-get install -y \
    git docker.io \
    && rm -rf /var/lib/apt/lists/*

# Add /usr/bin to PATH explicitly
# ENV PATH="/usr/bin:$PATH"

# Set the working directory in the container
# this allows for any subsequent commands to be run from this directory
WORKDIR /app

# Copy the current directory contents into the container at /app
# . indicates the directory where the Dockerfile is located and copies all 
# files in that directory into our container working directory
COPY . /app

# Install any needed packages specified in requirements.txt
# using --no-cache-dir to not cache the packages and save space
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4465 available to the world outside this container
EXPOSE 4465

#a more secure option would be to specify the exact IP you plan to use 
# (e.g.API gateway interface)
CMD ["squirrels", "run", "--host=0.0.0.0", "--port=4465"]