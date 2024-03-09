dockerd-rootless-setuptool-to-tmp.sh

docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

docker run --name mediaDB -p 5500:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgres -d postgres
