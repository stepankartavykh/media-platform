dockerd-rootless-setuptool-to-tmp.sh

docker run -d --name redis-first-storage -p 6379:6379 redis/redis-stack-server:latest
docker run -d --name redis-second-storage -p 6378:6379 redis/redis-stack-server:latest

docker run --name mediaDB -p 5500:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgres -d postgres
