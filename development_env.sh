#!/bin/bash

if ! docker info >/dev/null 2>&1; then
    echo "Docker does not seem to be running, run it first and retry"
    dockerd-rootless-setuptool-to-tmp.sh
else
    echo "Docker is launched!"
fi

docker ps
docker stop mediaConfigDatabase
docker rm mediaConfigDatabase

docker volume rm $(docker volume ls -qf dangling="true")

docker compose --verbose up -d

python_executor=$(which python)

echo "${python_executor}"

if [ -z "$python_executor" ]; then
  echo "Error with choosing python interpreter"
  exit 1
fi

"$python_executor" ./DataApp/storage_schemas/storage.py

echo "Databases and cache storage setup is completed!"
