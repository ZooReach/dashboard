#!/usr/bin/env bash

docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
docker build $NO_CACHE_OPTION -t dashboard_dev ./app
docker tag dashboard_dev zooreach12/dashboard_dev
docker push zooreach12/dashboard_dev
docker logout
echo "pushed into docker hub"
