SCRIPTS_DIR := ./scripts
DOCKER_COMPOSE_DIR := .

DUMP_DIR ?= ./storage/database_dumps
TIMESTAMP := $(shell date +"%Y-%m-%d-%H-%M-%S-%N")

python_executor=$(which python)


make_storage_dump:
	@echo "making dump..."
	@pg_dump --file=$(DUMP_DIR)/storage_dump_$(TIMESTAMP).sql --dbname=storage --username=admin --host=localhost --port=5500
