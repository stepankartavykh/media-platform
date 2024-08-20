#!/bin/bash

if ! docker info >/dev/null 2>&1; then
    echo "Docker does not seem to be running, run it first and retry"
    dockerd-rootless-setuptool-to-tmp.sh
else
    echo "Docker is launched!"
fi

docker compose up -d

sleep 1

./scripts/dump_load.sh

echo "Databases and cache storage setup is completed!"
