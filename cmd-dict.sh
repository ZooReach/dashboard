#!/usr/bin/env bash

set -e

function dockerHubPush {
	set -e
	DOCKER_USERNAME=$DOCKER_USERNAME \
	DOCKER_PASSWORD=$DOCKER_PASSWORD \
	./docker-hub-push.sh
}

function deploy {
	set -x

	ls -al ~/.ssh/

	which -a ssh

	which ssh

	ssh $USER@$BOX -o StrictHostKeyChecking=false  "
		(docker container stop \$(docker container ls -q) || echo 'no containers to stop') && 
		(docker container rm \$(docker container ls -q) || echo 'no containers to remove') && 
		(docker image rm \$(docker image ls -q) || echo 'no images to remove') &&
		(docker run -d --rm -p 80:5000 zooreach12/dashboard_dev) &&
		echo 'Deployed success'"

	echo "Deployed message from travis"
}

function unittest {
    set -e
    pip install -r requirements_test.txt
    pytest -v
}

function generate_visual_map {
	set -e
	pip install -r requirements_test.txt
	GITHUB_TOKEN=$GITHUB_TOKEN
	python -m scripts.create_species_metadata_map "$GITHUB_TOKEN"
}

function visual_metadata_dump {
   set -e
   pip install -r requirements_test.txt
   python -m scripts.visual_metadata_db_dump
}

case "$1" in 
	dockerHubPush) dockerHubPush ;;
	deploy) deploy ;;
	unittest) unittest ;;
	generate_visual_map) generate_visual_map ;;
	visual_metadata_dump) visual_metadata_dump ;;
esac
