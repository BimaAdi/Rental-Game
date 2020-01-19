# How To Use

## Requirement

python version 3.6

## Instalation
1. clone or download repository
1. open terminal/command promt on cloned/downloded repository.
1. `pip install -r requirements.txt` or `pip3 install -r requirements.txt` if you use mac or linux without virtual environtment.
1. Create database named rental (if you use mysql, Postgresql or oracle sql).
1. install database adapter, you can see available adapter at [list adapter](https://docs.sqlalchemy.org/en/13/core/engines.html) (defaul pymysql pre installed). Skip this step if you use sqlite.
1. Edit config.py based on your database.
1. run `python init.py` or `pip3 init.py`.
1. `export FLASK_APP=app.py` or `set FLASK_APP=app.py` if you use windows.

## Run the application
1. run `flask run`.
1. to stop just `ctrl + c`.
