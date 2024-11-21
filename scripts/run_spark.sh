#!/bin/bash

if ! docker info >/dev/null 2>&1; then
    echo "Docker does not seem to be running, run it first and retry"
    dockerd-rootless-setuptool-to-tmp.sh
else
    echo "Docker is launched!"
fi

docker kill spark-master spark-worker1 spark-submit
docker rm spark-master spark-worker1 spark-submit

docker stop spark-master || true && docker rm spark-master || true
docker stop spark-worker1 || true && docker rm spark-worker1 || true
docker stop spark-submit || true && docker rm spark-submit || true


docker network create -d bridge spark-network

docker run -dit --name spark-master --network spark-network -p 8080:8080 sdesilva26/spark_master

docker run -dit --name spark-worker1 --network spark-network -p 8081:8081 -e MEMORY=2G -e CORES=1 sdesilva26/spark_worker


docker run -dit --name spark-submit --network spark-network -p 4040:4040 sdesilva26/spark_submit