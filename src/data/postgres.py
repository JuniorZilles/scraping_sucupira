import psycopg2
from .db_config import Config

class PostgresClient(Config):
    def __init__(self):
        super().__init__()
        self.client = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)

    def no_result_connection_db(self, query, values) -> bool:
        try:
            cursor = self.client.cursor()
            cursor.execute(query, values)
            self.client.commit()
            cursor.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
    
    def close(self):
        if self.client is not None:
                self.client.close()

    def one_column_connection_db(self, query, values):
        db_result = None 
        try:
            cursor = self.client.cursor()
            cursor.execute(query, values)
            db_result = cursor.fetchone()
            if db_result != None:
                db_result = db_result[0]
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return db_result

    def one_row_connection_db(self, query, values):
        db_result = None
        try:
            cursor = self.client.cursor()
            cursor.execute(query, values)
            db_result = cursor.fetchone()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return db_result
    
    def all_rows_connection_db(self, query, values):
        dt_rows = None
        try:
            with self.client.cursor() as cur:
                cur.execute(query, values)
                dt_rows = cur.fetchall()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return dt_rows

    def all_rows_without_entry_connection_db(self, query):
        dt_rows = None
        try:
            with self.client.cursor() as cur:
                cur.execute(query)
                dt_rows = cur.fetchall()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return dt_rows