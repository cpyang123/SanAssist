install:
	pip install -r requirements.txt

test:
	find ./src/tests -name "*test*.py" -exec python -m pytest --nbval -v {} +
	
lint:
	ruff check
pylint:
	find ./src -name "*.py" -exec pylint --disable=R,C {} +
format:
	find ./src -name "*.py" -exec black {} +

all: install test lint format

# Define the image name
IMAGE_NAME = squirrels-app
DOCKER_ID_USER = nathan46

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -p 4465:4465 $(IMAGE_NAME)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

image_show:
	docker images

container_show:
	docker ps

push:
	docker login
	docker tag $(IMAGE_NAME) $(DOCKER_ID_USER)/$(IMAGE_NAME)
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME):latest

login:
	docker login -u ${DOCKER_ID_USER}