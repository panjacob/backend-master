from peewee import *
from database import db


def create_tables():
    with db:
        db.create_tables([Name, Coordinates, Timezone, Street, Location, Login, Dob, Registered, Id, Person])


class BaseModel(Model):
    class Meta:
        database = db


class Name(BaseModel):
    title = CharField()
    first = CharField()
    last = CharField()


class Coordinates(BaseModel):
    latitude = CharField()
    longitude = CharField()


class Timezone(BaseModel):
    offset = CharField()
    description = CharField()


class Street(BaseModel):
    number = CharField()
    name = CharField()


class Location(BaseModel):
    street = ForeignKeyField(Street, backref='locations')
    city = CharField()
    state = CharField()
    country = CharField()
    postcode = CharField()
    coordinates = ForeignKeyField(Coordinates, backref='locations')
    timezone = ForeignKeyField(Timezone, backref='locations')


class Login(BaseModel):
    uuid = CharField()
    username = CharField()
    password = CharField()
    salt = CharField()
    md5 = CharField()
    sha1 = CharField()
    sha256 = CharField()


class Dob(BaseModel):
    date = CharField()
    age = CharField()
    days_to_birthday = CharField()


class Registered(BaseModel):
    date = CharField()
    age = CharField()


class Id(BaseModel):
    name = CharField()
    value = CharField()


class Person(BaseModel):
    gender = CharField()
    name = ForeignKeyField(Name, backref='people')
    location = ForeignKeyField(Location, backref='people')
    email = CharField()
    login = ForeignKeyField(Login, backref='people')
    dob = ForeignKeyField(Dob, backref='people')
    registered = ForeignKeyField(Registered, backref='people')
    phone = CharField()
    cell = CharField()
    id = ForeignKeyField(Id, backref='people')
