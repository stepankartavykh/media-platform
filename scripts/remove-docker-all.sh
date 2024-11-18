#!/bin/bash

docker stop `docker ps -qa`

docker rm `docker ps -qa`

docker rmi -f `docker images -qa `

docker volume rm $(docker volume ls -qf dangling="true")

docker network rm `docker network ls -q`
