import sqlite3 as sl

class DB:
    def __init__(self, db_path, timeout=10):
        self.path = db_path
        self.timeout = timeout

    def __enter__(self):
        self.connection = sl.connect(self.path, timeout=self.timeout)
        return self.connection
  
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type != None:
            print(f"Error Type: {exc_type}, Value: {exc_value}")
        self.connection.close()
