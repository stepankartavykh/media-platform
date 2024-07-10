#!/bin/bash

docker compose up -d

sleep 1

./scripts/dump_load.sh

echo "Database setup is completed!"
