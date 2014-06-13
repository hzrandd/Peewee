import datetime
import math
import os
import random
import string
from datetime import date
from peewee import *


db = SqliteDatabase('people.db')


class Person(Model):
    name = CharField()
    birthday = DateField()
    deleted = BooleanField()
    delete_at = DateField()
    create_at = DateField()
    is_relative = DateField()

    class Meta:
        # this model uses the people database
        database = db


class Pet(Model):
    owner = ForeignKeyField(Person, related_name='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        # this model uses the people database
        database = db


def create_person_table():
    if Person.table_exists():
        Person.drop_table()
    Person.create_table()


def create_pet_table():
    if Pet.table_exists():
        Pet.drop_table()
    Pet.create_table()


def add_person(name):
    uncle_bob = Person(name=name, birthday=date(1960, 1, 15), deleted=False,
                       delete_at=datetime.datetime.utcnow(),
                       create_at=datetime.datetime.utcnow(),
                       is_relative=True)
    uncle_bob.save()
    return uncle_bob


def gen_random_string(lenth=8):
    return ''.join([(string.ascii_letters + string.digits)[x] for x in \
             random.sample(range(0, 62), lenth)])


def auto_string(lenth=5):
    return ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(8)))


def add_persons(counts=5):
    for i in range(counts):
        add_pet(gen_random_string(1))


def add_pet(name, animal_type='cat'):
    bob_kitty = Pet.create(owner=add_person(name), name=name,
                           animal_type=animal_type)
    bob_kitty.save()


def add_pets(counts=5):
    for i in range(counts):
        add_pet(gen_random_string())


def list_person_pets():
    for person in Person.select():
        print person.name, 'has', person.pets.count(), 'pets'
        for pet in person.pets:
            print ' ', 'pet name:', pet.name, ', pet type: ', pet.animal_type


def list_animal_by_type(animal_type='cat'):
    for pet in Pet.select().where(Pet.animal_type == animal_type):
        print pet.name, ' onwerd to ', pet.owner.name


def get_person_by_startwith(startwith, limit=10, offset=0):
    'paging to keep effective'
    persons = {}
    query = Person.select()
    query = query.where(fn.Lower(fn.Substr(Person.name, 1, 1)) ==
                        startwith)
    counts = query.count()
    persons['counts'] = counts
    persons['pages'] = int(math.ceil(counts / float(limit)))
    query = query.offset(offset).limit(limit)
    for person in query:
        persons[person.name] = person.create_at
    return persons


def get_person(name):
    query = Person.select().where(Person.name == name)
    result = query.get()
    return result


def get_pet(name):
    query = Pet.select()
    re = query.where(Pet.name == name).get()
    return re


def main():
    create_person_table()
    create_pet_table()
    add_persons()
    add_pets()
    list_animal_by_type()
    list_person_pets()
    print get_person_by_startwith('a')


if __name__ == '__main__':
    main()
