from peewee import *

db = SqliteDatabase(':memory:')

class Person(Model):
    name = CharField()
    class Meta:
        database = db

# let's pretend we want to do an "upsert", something that SQLite can
# do, but peewee cannot.
Person.create_table()
for name in ('charlie', 'mickey', 'huey'):
    db.execute_sql('REPLACE INTO person (name) VALUES (?)', (name,))

# now let's iterate over the people using our own query.
for person in Person.raw('select * from person'):
    import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
    print person.name  # .raw() will return model instances.

