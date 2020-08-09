from peewee import *
import os.path


db_name = 'people.db'
db = SqliteDatabase(db_name)


def is_db_exist():
    return os.path.isfile(db_name)


def before_db():
        db.connect()


def after_db():
    db.close()


