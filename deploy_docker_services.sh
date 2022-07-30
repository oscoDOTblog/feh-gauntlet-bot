#!/bin/bash

# Copy Secret Credentials to Mounted Volume
echo "Attempting to copy secret credentials..."
cp secrets.py assets/
echo "Successfully copied secret credentials!"

# Run Latest Docker Images
echo "Attempting to update Docker images..."
docker compose down
docker compose build
docker compose up -d
docker compose -f docker-compose.yml restart genny
docker compose -f docker-compose.yml restart rebecca
echo "Successfully updated Docker images!"