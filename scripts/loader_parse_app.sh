#!/bin/bash

if ! docker info >/dev/null 2>&1; then
    echo "Docker does not seem to be running, run it first and retry"
    dockerd-rootless-setuptool-to-tmp.sh
else
    echo "Docker is launched!"
fi


docker build ./DataApp/pyspark-loader/parse -t parse-app-image
docker run -d --name parse-app -p 8005:8000 parse-app-image
