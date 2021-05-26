#!/usr/bin/env python3
####################################################################################
#   sqlite controller
#   - creating new db
#   - insert or remove new rows
#   - swap rows
####################################################################################

import os
from time import sleep
import sqlite3 as sl

class SQL_Controller:
    def __init__(self):
        # db schema
        self.db = {
            'name': 'Users',
            'path': "users.db", 
            'columns': [
                {'name':'id', 'type': 'INTEGER'}, 
                {'name':'username', 'type': 'TEXT'}, 
                {'name':'status', 'type': 'TEXT'}
            ]
        }
        # create db if not exist in path
        if not os.path.exists(self.db['path']):
            self._create_db(self.db)  

    ''' Create new db '''
    def _create_db(self, db_obj):
        sql = "CREATE TABLE " + db_obj['name'] + " ("
        col_index = 0
        for col in db_obj['columns']:
            if col_index == 0:
                sql += col['name'] + " " + col['type'] + "  NOT NULL PRIMARY KEY AUTOINCREMENT,"
            else:
                sql += col['name'] + " " + col['type'] + ","
            col_index +=1
        sql = sql[:-1] + ");"
        self._send(db_obj, sql)

    ''' send sql to db '''
    def _send(self, db, sql, data=(), get=False):
        records = []
        con = sl.connect(db['path'], timeout=10)
        try:
            with con:
                numOfArgs = len(data)
                if get:
                    cur = con.cursor()
                    if numOfArgs:
                        cur.execute(sql, data)
                    else:
                        cur.execute(sql)
                    records = cur.fetchall()
                else:
                    if numOfArgs:
                        con.execute(sql, data)
                    else:
                        con.execute(sql)
                con.commit()
        except sl.Error as error:
            print(str(error))
        finally:
            if (con):
                con.close()
        return records

    ''' insert new row to db '''
    def _insert(self, db, data):
        if len(data) == len(db['columns']):
            sql = "INSERT INTO " + db['name'] + " ("
            for col in db['columns']:
                sql += col['name'] + ","
            sql = sql[:-1] + ") VALUES("
            for val in data:
                sql += "?,"
            sql = sql[:-1] + ");"
            self._send(db, sql, data=tuple(data))

    ''' remove row from db ''' 
    def _remove(self, db, location={'column': None, 'value': None, 'eq': True}):
        hasData = False
        sql = "DELETE FROM " + db['name']
        if location['column'] != None:
            hasData = True
            sql += " WHERE " + location['column']
            if location['eq']:
                sql += " = ?" 
            else:
                sql += " != ?" 
        sql += ";"
        if hasData:
            data = (location['value'],)
            self._send(db, sql=sql, data=data)
        else:
            self._send(db, sql=sql)

    ''' get data from db '''
    def _get(self, db, vals=[], location={'column': None, 'value': None, 'eq': True}, sort={'column': None, 'order': 'ASC'}):
        hasData = False
        sql = "SELECT "
        if len(vals):
            for val in vals:
                sql += val + ","
            sql = sql[:-1]
        else:
            sql += "*"
        sql += " FROM " + db['name']
        if location['column'] != None:
            hasData = True
            sql += " WHERE " + location['column']
            if location['eq']:
                sql += " = ?" 
            else:
                sql += " != ?" 
        if sort['column'] != None:
            sql += " ORDER BY " + sort['column'] + " " + sort['order']
        sql += ";"
        records = []
        if hasData:
            data = (location['value'],)
            records = self._send(db, sql, data, get=True)
        else:
            records = self._send(db, sql, get=True)  
        return records
    
    ''' set data in db row '''
    def _set(self, db, settings, location = {'column': None, 'value': None, 'eq': True}):
        data = []
        hasData = False
        sql = 'UPDATE ' + db['name'] + " SET "
        for val in settings:
            if val['const']:
                sql += val['column'] + " = " + val['value'] + "," 
            else:
                data.append(val['value'])
                sql += val['column'] + " = ?," 
        sql = sql[:-1] 
        if location['column'] != None:
            hasData = True
            sql += " WHERE " + location['column']
            if location['eq']:
                sql += " = ?" 
            else:
                sql += " != ?" 
        sql += ";"
        if hasData:
            data.append(location['value'])
        if len(data):
            data = tuple(data)
            self._send(db, sql, data, remote_upload=True)
        else:
            self._send(db, sql, remote_upload=True)

    ''' Swap values between rows '''
    def _swap(self, db, column, old, new):
        self._set(db, settings=[{'column':column, 'value': new, 'const': False}], location={'column': column, 'value': old, 'eq': True})
        self._set(db, settings=[{'column':column, 'value': old, 'const': False}], location={'column': column, 'value': new, 'eq': True})

    ''' Examples '''
    # add user to db
    def add_user(self, id, username, status):
        data = [id, username, status]
        self._insert(self.db, data)

    # get user by username
    def get_user(self, username): 
        return self._get(self.db, location={'column':'username', 'value': username, 'eq': True})

    # get all users
    def get_all_users(self):
        return self._get(self.db)

    # remove user
    def remove_user(self, id):
        self._remove(self.db, location={'column':'id', 'value': id, 'eq': True})

    # remove all users
    def clear_all_users(self):
        self._remove(self.db)
