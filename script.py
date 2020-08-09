from database import *
from scriptfunctions import *
from person import create_tables
import click

if is_db_exist():
    before_db()
else:
    before_db()
    create_tables()
    print("Utworzono nową bazę danych")


@click.group()
def cli():
    pass


@cli.command(name='insert-offline')
@click.argument('filename', type=str, default='persons.json')
def cli_insert_offline(filename):
    json = get_local_json(filename)
    insert_data_from_json(json)
    print("zakończono!")


@cli.command(name='insert-online')
@click.argument('number', type=int, default='persons.json')
def cli_insert_online(number):
    print('pobieranie...')
    insert_data_online(number)
    print("zakończono!")


@cli.command(name='remove-db')
@click.argument('filename', type=str, default='people.db')
def cli_remove_db(filename):
    remove_db(filename)


@cli.command(name='gender')
def cli_gender_percent():
    if_db_empty_exit()
    print(gender_percent())


@cli.command(name='average-age')
@click.argument('gender', type=str, default='a')
def cli_average_age(gender):
    if_db_empty_exit()
    print(average_age(gender))


@cli.command(name='most-common-cities')
@click.argument('limit', type=int, default=1)
def cli_most_common_cities(limit):
    if_db_empty_exit()
    print_pretty(get_most_common_cities(limit))


@cli.command(name='most-common-passwords')
@click.argument('limit', type=int, default=1)
def cli_most_common_passwords(limit):
    if_db_empty_exit()
    print_pretty(get_most_common_passwords(limit))


@cli.command(name='most-secure-passwords')
@click.argument('limit', type=int, default=1)
def cli_most_secure_passwords(limit):
    if_db_empty_exit()
    print_pretty(get_most_secure_passwords(limit))


@cli.command(name='born-between')
@click.argument('start', type=str, default='1970-01-01')
@click.argument('end', type=str, default='2020-01-01')
def cli_people_born_between_dates(start, end):
    if_db_empty_exit()
    print_people_born_between_dates(start, end)


if __name__ == '__main__':
    cli()

after_db()
