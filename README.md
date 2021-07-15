# SQL Controller

an module to easily manage sqlite3 db.  \

## Usage

Change `db_config.py` values to match your db values.

```
    /* Create new database via sqlite3 */
    from src.db_controller import DBController
    from src.db_config import DBConfig

    controller = DBController(DBConfig)
    row = ['user', 'pending']   # auto assigned row[0] to id value 
    controller.add_row(row)
    res = controller.get_all()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
