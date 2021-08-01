from db.sql_maker import SQLMaker
from db.db_context import DB
import os

class DBController:
    def __init__(self, config):
        self.db_name = config.name
        self.db_path = config.path
        self.sql = SQLMaker(self.db_name, config.columns)
        # create db if not exist in path
        if not os.path.exists(self.db_path):
            self._init_db() 

    ''' send sql to db '''
    def _send(self, sql_info, get=False):
        records = []
        sql = sql_info[0]
        data = sql_info[1]
        with DB(self.db_path, timeout=10) as con:
            if get:
                cur = con.cursor()
                if len(data):
                    cur.execute(sql, data)
                else:
                    cur.execute(sql)
                records = cur.fetchall()
            elif len(data):
                con.execute(sql, data)
            else:
                 con.execute(sql)
            con.commit()
            
        return records
        
    ''' Crate db table '''
    def _init_db(self):
        sql = self.sql.create()
        self._send(sql)
    
    def get_last_id(self):
        # get last id
        last_id = 1000
        sql = self.sql.select(values=['id'])
        res = self._send(sql, get=True)
        print(res)
        if len(res):
            last_id = res[-1][0]
        return last_id
    
    ''' Add row '''
    def add_row(self, row):
        uid = self.get_last_id() + 1
        row.insert(0,uid)
        sql = self.sql.insert(row)
        self._send(sql)

    ''' Remove row'''
    def remove_row(self, uid):
        sql = self.sql.delete(where={'column': 'id', 'value': uid, 'eq': True})
        self._send(sql)

    ''' Get rows by column'''
    def get_row_by_column(self, column, value): 
        sql = self.sql.select(where={'column': column, 'value': value, 'eq': True})
        return self._send(sql, get=True)

    ''' Get all rows '''
    def get_all(self):
        sql = self.sql.select()
        return self._send(sql, get=True)

    ''' Remove all rows '''
    def clear_all(self):
        sql = self.sql.delete()
        self._send(sql)
    