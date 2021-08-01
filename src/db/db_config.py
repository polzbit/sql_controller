
class DBConfig:
    name = 'mydb'
    path = 'mydb.db'
    columns = [
        {'name':'id', 'type': 'INTEGER'}, 
        {'name':'username', 'type': 'TEXT'}, 
        {'name':'status', 'type': 'TEXT'}
    ]
    