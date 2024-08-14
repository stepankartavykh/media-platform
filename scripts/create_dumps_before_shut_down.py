import os
import subprocess
import psycopg2

db_host = "localhost"
db_name = "storage"
db_user = "admin"
db_password = "password"

tables_to_dump = ["articles.articles", "parsed.packets"]

dump_dir = "/home/skartavykh/MyProjects/media-bot/storage"

os.makedirs(dump_dir, exist_ok=True)
with psycopg2.connect(host=db_host,
                      port=5500,
                      database=db_name,
                      user=db_user,
                      password=db_password) as connection:
    cursor = connection.cursor()
    for table in tables_to_dump:
        dump_command = f"pg_dump -t {table} -f {os.path.join(dump_dir, table + '.sql')} {db_name}"
        try:
            subprocess.run(dump_command, shell=True, check=True)
            print(f"Dumped table {table} to {os.path.join(dump_dir, table + '.sql')}")
        except subprocess.CalledProcessError as e:
            print(f"Error dumping table {table}: {e}")
    cursor.close()
