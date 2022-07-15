# Set Docker Image Version
export DOCKER_VERSION=1.61

# Build, Deploy, and Tear Down Docker Containers
echo "Attempting to build Docker containers..."
docker build -t feh-gauntlet-bot_convoy ./convoy/
docker build -t feh-gauntlet-bot_genny ./discord/genny/
docker build -t feh-gauntlet-bot_rebecca ./discord/rebecca/

echo "----------Success!!!----------"

# Log Into Docker
echo "Attempting to log into Docker..."
docker login
echo "----------Success!!!----------"

# Upload Latest Convoy Image
echo "Attempting to upload latest Convoy images..."
docker tag feh-gauntlet-bot_convoy atemosta/feh-gauntlet-bot:convoy-${DOCKER_VERSION}
docker push atemosta/feh-gauntlet-bot:convoy-${DOCKER_VERSION}
docker tag feh-gauntlet-bot_convoy atemosta/feh-gauntlet-bot:convoy-latest
docker push atemosta/feh-gauntlet-bot:convoy-latest
echo "----------Success!!!----------"

# Upload Latest Genny Image
echo "Attempting to upload latest Genny images..."
docker tag feh-gauntlet-bot_genny atemosta/feh-gauntlet-bot:genny-${DOCKER_VERSION}
docker push atemosta/feh-gauntlet-bot:genny-${DOCKER_VERSION}
docker tag feh-gauntlet-bot_genny atemosta/feh-gauntlet-bot:genny-latest
docker push atemosta/feh-gauntlet-bot:genny-latest
echo "----------Success!!!----------"

# Upload Latest Rebecca Image
echo "Attempting to upload latest Rebecca images..."
docker tag feh-gauntlet-bot_rebecca atemosta/feh-gauntlet-bot:rebecca-${DOCKER_VERSION}
docker push atemosta/feh-gauntlet-bot:rebecca-${DOCKER_VERSION}
docker tag feh-gauntlet-bot_rebecca atemosta/feh-gauntlet-bot:rebecca-latest
docker push atemosta/feh-gauntlet-bot:rebecca-latest
echo "----------Success!!!----------"


# Clear Docker Containers and Images (Optional)
# echo "Clearing old docker images..."
# docker stop $(docker ps -a -q)
# docker rm $(docker ps -a -q)
# export IMAGE_PATTERN=feh-gauntlet-bot
# docker images -a |  grep ${IMAGE_PATTERN}
# docker images -a | grep ${IMAGE_PATTERN} | awk '{print $3}' | xargs docker rmi -f
# echo "----------Success!!!----------"
