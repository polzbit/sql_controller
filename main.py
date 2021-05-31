from sql_controller import SQL_Controller

class UsersDb(SQL_Controller):
    def __init__(self):
        users_db = {
            'name': 'Users',
            'path': "users.db", 
            'columns': [
                {'name':'id', 'type': 'INTEGER'}, 
                {'name':'username', 'type': 'TEXT'}, 
                {'name':'status', 'type': 'TEXT'}
            ]
        }
        super().__init__(users_db)
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

    