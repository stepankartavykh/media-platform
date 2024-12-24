SCRIPTS_DIR := ./scripts
DOCKER_COMPOSE_DIR := .

DUMP_DIR ?= ./storage/database_dumps
TIMESTAMP := $(shell date +"%Y-%m-%d-%H-%M-%S-%N")

python_executor=$(which python)


make_storage_dump:
	@echo "making dump..."
	@pg_dump --file=$(DUMP_DIR)/storage_dump_$(TIMESTAMP).sql --dbname=storage --username=admin --host=localhost --port=5500


create_loader_container:
	@/bin/bash ./scripts/loader_parse_app.sh


reload_parser_app:
	@docker stop parse-app
	@docker rm parse-app
	@docker build ./DataApp/pyspark-loader/parse -t parse-app-image
	@docker run -d --name parse-app -p 8005:8000 parse-app-image

launch_compose_file:
	@docker compose -f compose-test.yml --verbose up -d