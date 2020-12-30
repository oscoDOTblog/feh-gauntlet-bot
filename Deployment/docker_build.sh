# Set Up
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# Test and Build
docker build -t atemosta/feh-gauntlet-bot .
docker run -it atemosta/feh-gauntlet-bot /bin/bash

# Clean Containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# Upload
docker login atemosta
docker tag atemosta/feh-gauntlet-bot atemosta/feh-gauntlet-bot:v1.0
docker push atemosta/feh-gauntlet-bot:v1.0

# Debugging
docker inspect <container-id>
docker logs <container-id>
docker stop <container-id>