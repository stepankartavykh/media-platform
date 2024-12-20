FROM python:3.12


WORKDIR /app-code


COPY ./requirements.txt /app-code/requirements.txt
COPY ./warc-files-for-debug-parse-app /tmp


RUN apt-get update && apt-get install -y htop
RUN apt-get install ca-certificates
RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get update && apt-get install -y telnet


RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir --upgrade -r /app-code/requirements.txt
RUN python -m pip install --upgrade certifi

COPY ./app.py /app-code/app.py
COPY ./test_parse.py /app-code/test_parse.py
COPY ./data_loader.py /app-code/data_loader.py
COPY ./db_manager.py /app-code/db_manager.py
COPY ./db_models.py /app-code/db_models.py
COPY ./.env /app-code/.env

CMD ["fastapi", "run", "/app-code/app.py", "--port", "8000"]


# docker build . -t parse-app-image
# docker run -d --name parse-app -p 8005:8000 parse-app-image
