from db.db_controller import DBController
from db.db_config import DBConfig

def main():
    controller = DBController(DBConfig)
    row = ['user', 'pending']
    controller.add_row(row)
    res = controller.get_all()
    print(res)

if __name__ == "__main__":
    main()