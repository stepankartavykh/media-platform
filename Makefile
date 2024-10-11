local-env:
	@echo 'wer'
	sleep 1
	@if ! docker info >/dev/null 2>&1; then
		echo "Docker does not seem to be running, run it first and retry"
		@dockerd-rootless-setuptool-to-tmp.sh
	@else
		echo "Docker is launched!"
	fi

	sleep 1

	docker compose up -d

	sleep 1

	./scripts/dump_load.sh

	./env/bin/python ./DataApp/storage_schemas/storage.py

	echo "Databases and cache storage setup is completed!"

SCRIPTS_DIR := ./scripts
DOCKER_COMPOSE_DIR := .

test:
	@if [! docker info >/dev/null 2>&1]; then\
		@echo "Docker does not seem to be running, run it first and retry";\
	fi

launch-docker:
	if ! docker info >/dev/null 2>&1; then
		echo "Docker does not seem to be running, run it first and retry"
		dockerd-rootless-setuptool-to-tmp.sh
	else
		echo "Docker is launched!"
	fi


test:
	echo $LANG
	if [ 1 > 2 ]; then
	  echo "Empty"
	else
	  echo "Not empty"
	fi



check:
    if [ -z "$(APP_NAME)" ]; then \
        echo "Empty"; \
    else \
        echo "Not empty"; \
    fi


print:
	@echo "print in print staements"
	echo "This line will print if the file hello does not exist."


local-env:
	./development_env.sh


get-containers:
	@docker ps


some_file_create:
	touch some_file


files := file1 file2
cur_dir := $(PWD)
parser_relative_path_app := /DataApp/pyspark-loader/parse/app.py

parser_dir := $(cur_dir)$(parser_relative_path_app)

some_file:
	echo "Look at this variable: " $(files)
	touch some_file

file1:
	echo "Current directory is: " $(cur_dir)
	touch file1

file2:
	touch file2


dirs: check_file
	@echo
	@echo "Current directory is: " $(cur_dir)
	@echo "Dir with parser  for WARC file is: " $(parser_dir)
	@echo


check_file:
	ifneq ("$(wildcard $(parser_dir))","")
		FILE_EXISTS = 1
	else
		FILE_EXISTS = 0
	endif

some_commands:
	OUTPUT="$(which python)"
	@echo "$OUTPUT"



clean:
	rm file1 file2 some_file 1 2


install-libs:
	which pip
	pip install fastapi