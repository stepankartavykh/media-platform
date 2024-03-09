FROM python

WORKDIR /app

COPY . .

RUN source env/bin/activate
RUN pip install -r reqs.txt

COPY . .

CMD ["python", "main.py"]
