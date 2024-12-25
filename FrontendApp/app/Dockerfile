FROM python:3.12


WORKDIR /frontend-app-code


COPY ./reqs.txt /frontend-app-code/requirements.txt


RUN apt-get update && apt-get install -y htop
RUN apt-get install ca-certificates
RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get update && apt-get install -y telnet


RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-cache-dir --upgrade -r /frontend-app-code/requirements.txt

COPY ./app.py /frontend-app-code/app.py
COPY ./cache_plugin.py /frontend-app-code/cache_plugin.py
COPY ./connection_manager.py /frontend-app-code/connection_manager.py
COPY ./database_storage_plugin.py /frontend-app-code/database_storage_plugin.py

CMD ["fastapi", "run", "/app-code/app.py", "--port", "8000"]
