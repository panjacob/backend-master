import pytest
from scriptfunctions import *
import database
import os

def test_clear_phone_number():
    phone = "+123-x45-67/89--0"
    clean_phone_number = clear_phone_numbers(phone)
    assert clean_phone_number == "1234567890"

def test_remove_db():
    db_name = 'people.db'
    remove_db(db_name)
    assert os.path.isfile(db_name) == False

def test_create_db():
    database.before_db()
    database.after_db()
    assert os.path.isfile(database.db_name) == True


# def test_insert_data_offline():
#     database.before_db()
#     create_tables()
#     required_size = 1000
#     filename = 'persons.json'
#     json = get_local_json(filename)
#     insert_data_from_json(json)
#     assert get_db_size() == required_size

# def test_insert_data_online():
#     db_name = 'people.db'
#     remove_db(db_name)
#     database.before_db()
#     create_tables()
#     required_size = 10
#     insert_data_online(10)
#     assert get_db_size() == required_size

def test_check_password_strength_1():
    password = 'Abc123$de'
    points = check_password_strength(password)
    assert points == 13

def test_check_password_strength_2():
    password = 'abc123'
    points = check_password_strength(password)
    assert points == 3

