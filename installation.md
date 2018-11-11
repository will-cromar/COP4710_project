1. With a clean Python 3.7 environment, install the dependencies of the project from `requirements.txt` with `pip install -r requirements.txt`.

2. Start a new MySQL database accessible by user `root` with password `mypassword` and run the following SQL scripts in order in that database:
```
schema.sql
triggers.sql
views.sql
init_data.sql
demo_data.sql
```

3. Create a file at `instance/config.py` with the following content, filling in the MySQL host and DB name with the appropriate values.
```Python
DEBUG = True
SECRET_KEY = 'you-will-never-guess'
MYSQL_HOST = '...'
MYSQL_DB = '...'
```

4. Run `python run.py` to start the server.
