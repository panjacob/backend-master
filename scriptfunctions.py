import os
from person import *
import json
import datetime, calendar
import requests


def insert_class_from_json_name(name_json):
    title = name_json['title']
    first = name_json['first']
    last = name_json['last']
    name = Name.create(title=title, first=first, last=last)
    return name


def insert_class_from_json_location(location_json):
    street_json = location_json['street']
    coordinates_json = location_json['coordinates']
    timezone_json = location_json['timezone']
    number = street_json['number']
    name = street_json['name']

    street = Street.create(number=number, name=name)
    city = location_json['city']
    state = location_json['state']
    country = location_json['country']
    postcode = location_json['postcode']
    latitude = coordinates_json['latitude']
    longitude = coordinates_json['longitude']
    coordinates = Coordinates.create(latitude=latitude, longitude=longitude)
    offset = timezone_json['offset']
    description = timezone_json['description']
    timezone = Timezone.create(offset=offset, description=description)
    location = Location.create(street=street, city=city, state=state, country=country, postcode=postcode,
                               coordinates=coordinates, timezone=timezone)
    return location


def insert_class_from_json_login(login_json):
    uuid = login_json['uuid']
    username = login_json['username']
    password = login_json['password']
    salt = login_json['salt']
    md5 = login_json['md5']
    sha1 = login_json['sha1']
    sha256 = login_json['sha256']
    login = Login.create(uuid=uuid, username=username, password=password, salt=salt, md5=md5, sha1=sha1, sha256=sha256)
    return login


def calculate_days_to_birthday(date):
    today_date = datetime.datetime.today()
    converted_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    converted_date_to_calculate = datetime.datetime(today_date.year, converted_date.month, converted_date.day)
    delta = converted_date_to_calculate - today_date

    if delta.days >= 0:
        return delta.days
    else:
        return 365 + 1 * calendar.isleap(today_date.year + 1) + delta.days


def insert_class_from_json_dob(dob_json):
    date = dob_json['date']
    age = dob_json['age']
    days_to_birthday = calculate_days_to_birthday(date)
    dob = Dob.create(date=date, age=age, days_to_birthday=days_to_birthday)
    return dob


def insert_class_from_json_registered(registered_json):
    date = registered_json['date']
    age = registered_json['age']
    registered = Registered.create(date=date, age=age)
    return registered


def insert_class_from_json_id(id_json):
    name = id_json['name']
    value = id_json['value']
    if value is None:
        value = ""
    id = Id.create(name=name, value=value)
    return id


def clear_phone_numbers(phone):
    return ''.join(i for i in phone if i.isdigit())


def insert_class_from_json_person(person_json):
    name_json = person_json['name']
    location_json = person_json['location']
    login_json = person_json['login']
    dob_json = person_json['dob']
    registered_json = person_json['registered']
    id_json = person_json['id']

    gender = person_json['gender']
    name = insert_class_from_json_name(name_json)
    location = insert_class_from_json_location(location_json)
    email = person_json['email']
    login = insert_class_from_json_login(login_json)
    dob = insert_class_from_json_dob(dob_json)
    registered = insert_class_from_json_registered(registered_json)
    phone = person_json['phone']
    phone = clear_phone_numbers(phone)
    cell = person_json['cell']
    cell = clear_phone_numbers(cell)
    id = insert_class_from_json_id(id_json)
    nat = person_json['nat']

    person = Person.create(gender=gender, name=name, location=location, email=email, login=login, dob=dob,
                           registered=registered, phone=phone, cell=cell, id=id, nat=nat)
    return person


def get_local_json(filename):
    return json.load(open(filename, encoding="utf8"))


def insert_data_from_json(json):
    for person_json in json['results']:
        insert_class_from_json_person(person_json)


def gender_percent():
    people_count = Person.select().count()
    male = Person.select().where(Person.gender == 'male').count()
    female = Person.select().where(Person.gender == 'female').count()
    male_percent = male / people_count * 100
    female_percent = female / people_count * 100
    return "male:" + str(male_percent) + "%" + " female:" + str(female_percent) + "%"


def average_age(gender):
    if gender == 'f':
        people_count = Person.select().where(Person.gender == 'female').count()
        people = Person.select().where(Person.gender == 'female')
    elif gender == 'm':
        people_count = Person.select().where(Person.gender == 'male').count()
        people = Person.select().where(Person.gender == 'male')
    else:
        people_count = Person.select().count()
        people = Person.select()

    age_sum = 0
    for person in people:
        age_sum += int(person.dob.age)

    return age_sum / people_count


def print_pretty(things):
    for x in things:
        print(x + " " + str(things[x]))


def get_cities_from_people():
    people = Person.select()
    cities = []
    for person in people:
        cities.append(person.location.city)
    return cities


def get_passwords_from_people():
    people = Person.select()
    cities = []
    for person in people:
        cities.append(person.login.password)
    return cities


def sum_all_occurences_in_array(things):
    list = {}
    for thing in things:
        if thing not in list:
            list[thing] = 0
        if thing in things:
            list[thing] += 1
    return list


def add_sum_of_occurences_in_sorted_things(sorted_things, sum_of_all_occurences, limit):
    result = {}
    for thing in sorted_things[:limit]:
        result[thing] = sum_of_all_occurences[thing]
    return result


def most_common_list_of(things, limit):
    sum_of_all_occurences = sum_all_occurences_in_array(things)
    sorted_things = sorted(sum_of_all_occurences, key=sum_of_all_occurences.get, reverse=True)
    result = add_sum_of_occurences_in_sorted_things(sorted_things, sum_of_all_occurences, limit)
    return result


def get_most_common_passwords(limit):
    return most_common_list_of(get_passwords_from_people(), limit)


def get_most_common_cities(limit):
    return most_common_list_of(get_cities_from_people(), limit)


def str_to_date(str):
    return datetime.datetime.strptime(str, '%Y-%m-%d')


def str_to_date2(str):
    return datetime.datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ')


def get_people_born_between_dates(start, end):
    list = []
    people = Person.select()
    start = str_to_date(start)
    end = str_to_date(end)
    if start > end:
        start, end = end, start

    for person in people:
        birthday = str_to_date2(person.dob.date)
        if start <= birthday <= end:
            list.append(person)
    return list


def print_people_born_between_dates(start, end):
    list_of_people = get_people_born_between_dates(start, end)
    i = 0
    for person in list_of_people:
        birthday = str_to_date2(person.dob.date)
        print("id: " + str(person.id) + " first: " + str(person.name.first) + " birthday: " + str(birthday.date()))
        i += 1
    print("total: " + str(i))


def check_password_strength(password):
    points = 0
    if (any(x.islower() for x in password)):
        points += 1
    if (any(x.isupper() for x in password)):
        points += 2
    if (any(x.isdigit() for x in password)):
        points += 2
    if any(not x.isalnum() for x in password):
        points += 3
    if len(password) >= 8:
        points += 5
    return points


def get_passwords_with_points():
    passwords = get_passwords_from_people()
    list = {}
    for password in passwords:
        list[password] = check_password_strength(password)
    return list


def get_most_secure_passwords(limit):
    passwords = get_passwords_with_points()
    passwords_sorted = sorted_things = sorted(passwords, key=passwords.get, reverse=True)
    list = add_sum_of_occurences_in_sorted_things(passwords_sorted, passwords, limit)
    return list


def get_online_json(number):
    request = "https://randomuser.me/api/?results=" + str(number)
    r = requests.get(request)
    return r.json()


def remove_db(filename):
    db.close()
    os.remove(filename)


def get_db_size():
    people = Person.select()
    return len(people)


def if_db_empty_exit():
    if (get_db_size() <= 0):
        print('Baza danych jest pusta! Aby dodać:')
        print('insert-offline [nazwapliku]\ninsert-online [ile]')
        exit()


def insert_data_online(number):
    if number <= 0:
        number = 1
    elif number > 5000:
        number = 5000
    request = get_online_json(number)
    insert_data_from_json(request)
