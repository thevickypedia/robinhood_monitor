#!/bin/bash

# stops all existing docker containers
echo stopping containers
docker stop $(docker ps -a -q)

# deletes all existing docker containers
echo deleting containers
docker rm $(docker ps -a -q)

# force deletes all existing docker images
echo force deleting docker images
docker rmi $(docker images -q) -f

# docker images

# builds docker image robinhood with tag 1.0
echo bulding docker image
docker build -t robinhood:1.0 .

# runs the docker image
echo running docker
docker run robinhood:1.0