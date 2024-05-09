from config import DatabaseConfig
import psycopg2


class ConfigDatabase:
    def __init__(self):
        pass

    @staticmethod
    def check():
        with psycopg2.connect(dbname=DatabaseConfig.database_name.value,
                              host=DatabaseConfig.host.value,
                              user=DatabaseConfig.user.value,
                              password=DatabaseConfig.password.value,
                              port=DatabaseConfig.port.value) as connection:
            print('Connection to config database is established!')
