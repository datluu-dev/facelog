from datetime import datetime
import sqlite3
import json

class FacelogDbManager(object):
    def __init__(self, database):
        self.conn = None
        self.cursor = None

        if database:
            self.open(database)

    def open(self, database):
        try:
            self.conn = sqlite3.connect(database)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
    
    def create_data_table(self):
        self.conn.execute('\
            CREATE TABLE IF NOT EXISTS "FaceData" (\
                "img_id" INTEGER PRIMARY KEY AUTOINCREMENT, \
                "datetime" TEXT, \
                "path" TEXT \
            )\
        ')

    def get_from_table(self, table="FaceData", columns='*', order_val='datetime'):
        querry_code = """
                      select {0} from {1}
                      order by {2} desc
                      LIMIT 500
                      """.format(columns, table, order_val)
        self.cursor.execute(querry_code)
        return self.cursor.fetchall()

    def insert_to_db(self, table, data, columns):
        data_string = ""
        for d in data:
            data_string += f'"{d}",'
        querry_code = f"""
            insert into {table} ({columns})
            values
                ({data_string[:-1]})
        """
        # print(querry_code)
        self.cursor.execute(querry_code)
        self.conn.commit()