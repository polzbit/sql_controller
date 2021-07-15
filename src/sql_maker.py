
class SQLMaker:
    def __init__(self, table_name, table_columns):
        self.name = table_name
        self.columns = table_columns

    ''' Create table statement '''
    def create(self):
        sql = f"CREATE TABLE {self.name} ("
        for i, col in enumerate(iter(self.columns)):
            if i == 0:
                sql += f"{col['name']} {col['type']} NOT NULL PRIMARY KEY AUTOINCREMENT, "
            else:
                sql += f"{col['name']} {col['type']}, "
        return (f"{sql[:-2]});" , ())

    ''' insert rows statement '''
    def insert(self, data):
        if len(data) == len(self.columns):
            sql = f"INSERT INTO {self.name} (" 
            for col in iter(self.columns):
                sql += f"{col['name']},"
            sql = f"{sql[:-1]}) VALUES("

            for val in iter(data):
                sql += "?,"
            sql = f"{sql[:-1]});"
            return (sql , tuple(data))
        else:
            print("[(!) DB ] Insert failed, columns mismatch")

    ''' Delete Row '''
    def delete(self, where={'column': None, 'value': None, 'eq': True}):
        data = ()
        sql = f"DELETE FROM {self.name}"
        if where['column'] != None:
            data = (where['value'],)
            sql += f" WHERE {where['column']}"
            if where['eq']:
                sql += " = ?" 
            else:
                sql += " != ?" 
        sql += ";"
        return (sql, data)

    ''' Select rows '''
    def select(self, values=[], where={'column': None, 'value': None, 'eq': True}, sort={'column': None, 'order': 'ASC'}):
        data = ()
        sql = "SELECT "
        if len(values):
            for val in iter(values):
                sql += f"{val}, "
            sql = sql[:-2]
        else:
            sql += "*"
        sql += f" FROM {self.name}"
        if where['column'] != None:
            data = (where['value'],)
            sql += f" WHERE {where['column']}"
            if where['eq']:
                sql += " = ?" 
            else:
                sql += " != ?" 
        if sort['column'] != None:
            sql += f" ORDER BY {sort['column']} {sort['order']}"
        sql += ";"
 
        return (sql, data)

    ''' Update row '''
    def update(self, values, where={'column': None, 'value': None, 'eq': True}):
        data = []
        sql = f'UPDATE {self.name} SET '
        for val in iter(values):
            if val['const']:
                sql += f"{val['column']} = {val['value']}, " 
            else:
                data.append(val['value'])
                sql += f"{val['column']} = ?, " 
        sql = sql[:-2] 
        if where['column'] != None:
            data.append(where['value'])
            sql += f" WHERE {where['column']}"
            if where['eq']:
                sql += " = ?" 
            else:
                sql += " != ?" 
        sql += ";"

        return (sql , tuple(data))
        
