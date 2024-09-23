#!/bin/bash

if ! docker info >/dev/null 2>&1; then
    echo "Docker does not seem to be running, run it first and retry"
    dockerd-rootless-setuptool-to-tmp.sh
else
    echo "Docker is launched!"
fi

docker build -t frontend-app:latest ../frontend/.

docker run -d -p 8000:3000 --name frontend-app-container frontend-app:latest
