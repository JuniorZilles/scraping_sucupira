import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .schema import schemaList
from .db_config import Config


class DatabaseHandler(Config):
    def __init__(self):
        super().__init__()

    def exist_db(self):
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.password, database=self.database, connect_timeout=1)
            conn.close()
            return True
        except Exception as e:
            print('exist_db -> Exception -> ' + str(e))
            return False


    def create_db(self):
        try:
            # CRIA O BANCO
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.password)

            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(sql.SQL('''CREATE DATABASE {}
                                    WITH 
                                    OWNER = postgres
                                    ENCODING = 'UTF8'
                                    TABLESPACE = pg_default
                                    CONNECTION LIMIT = -1;''').format(
                                    sql.Identifier(self.database)))
            conn.commit()
            conn.close()

            # INCLUI NO BANCO AS TABELAS/SCHEMAS/FUNCOES
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.password, database=self.database)
            for query in schemaList:
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
                cur.close()
            conn.close()
            return True
        except Exception as e:
            print('create_db -> Exception -> ' + str(e))
            return False

