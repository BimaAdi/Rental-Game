SECRET_KEY = 'secretkey'
## database
# if using mysql/postgresql/oracle (uncomment this and fill the data)
dialect='mysql'
adapter = 'pymysql'
username = 'bima'
password = 'password'
host='localhost'
database='rental'
SQLALCHEMY_DATABASE_URI = f'{dialect}+{adapter}://{username}:{password}@{host}/{database}'

# if using sqlite (uncomment this)
# if using absolute path use double slash (//) instead of single slash
# path_to_db = '/database.db'
# SQLALCHEMY_DATABASE_URI = f'sqlite://{path_to_db}'
