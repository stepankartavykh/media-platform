SCRIPTS_DIR := ./scripts
DOCKER_COMPOSE_DIR := .

DUMP_DIR ?= ./storage/database_dumps
TIMESTAMP := $(shell date +"%Y-%m-%d-%H-%M-%S-%N")

python_executor=$(which python)


launch_docker:
	@bash -c '\
		if ! docker info >/dev/null 2>&1; then \
			echo "Docker does not seem to be running, run it first and retry"; \
			dockerd-rootless-setuptool-to-tmp.sh; \
		else \
			echo "Docker is launched!"; \
		fi'


make_storage_dump:
	@echo "making dump..."
	@pg_dump --file=$(DUMP_DIR)/storage_dump_$(TIMESTAMP).sql --dbname=storage --username=admin --host=localhost --port=5500


create_loader_container:
	@/bin/bash ./scripts/loader_parse_app.sh


reload_parser_app:
	@docker stop parser-app
	@docker rm parser-app
	@docker build ./DataApp/pyspark-loader/parse -t parser-app-image
	@docker run -d --name parser-app -p 8005:8000 parser-app-image


launch_compose_file:
	@docker compose -f compose-test.yml --verbose up -d


remove_compose_file:
	@docker compose -f compose-test.yml down


show_containers_ports:
	@docker ps --format '{{.Names}}\t\t{{.Ports}}'
