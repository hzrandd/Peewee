from peewee import *

# using with sqlite
custom_db = SqliteDatabase('custom.db')

class CustomModel(Model):
    '''
    Remember to specify a database in a model class (or its parent class),
    otherwise peewee will fall back to a default sqlite database named
    "peewee.db".

    Multi-threaded applications
    Some database engines may not allow a connection to be shared across
    threads, notably sqlite. If you would like peewee to maintain a single
    connection per-thread, instantiate your database with
    threadlocals=True (recommended):
    concurrent_db = SqliteDatabase('stats.db', threadlocals=True)
    With the above peewee stores connection state in a thread local; each
    thread gets its own separate connection.

    Alternatively, Python sqlite3 module can share a connection across
    different threads, but you have to
    disable runtime checks to reuse the single connection:

    concurrent_db = SqliteDatabase('stats.db', check_same_thread=False)

    CURD:
    url->http://peewee.readthedocs.org/en/latest/peewee/cookbook.html#cookbook
    '''
    class Meta:
        database = custom_db

class User(CustomModel):
    username = CharField()

class Tweet(CustomModel):
    #Changing autocommit behavior
    #By default, databases are initialized with autocommit=True,
    #you can turn this on and off at runtime if you like. The behavior below
    #is roughly the same as the context manager and decorator:

    def autocommit(self, tag=False):
        db.set_autocommit(tag)
        try:
            user.delete_instance(recursive=True)
        except:
            db.rollback()
            raise
        else:
            try:
                db.commit()
            except:
                db.rollback()
                raise
            finally:
                db.set_autocommit(not tag)

    '''
    If you would like to manually control every transaction,
    simply turn autocommit off when instantiating your database:
    '''
    def setautocommit(tag=False):
        db = SqliteDatabase(':memory:', autocommit=tag)

        User.create(username='somebody')
        db.commit()

# composite primary keys
class BlogToTag(Model):
    """
    Peewee has very basic support for composite keys. In order to use a
    composite key, you must set the primary_key attribute of the model
    options to a CompositeKey instance:
    A simple "through" table for many-to-many relationship."""
    blog = ForeignKeyField(Blog)
    tag = ForeignKeyField(Tag)

    class Meta:
        primary_key = CompositeKey('blog', 'tag')

# Bulk inserts
def bulk_insert()
    for data_dict in data_source:
    Model.create(**data_dict)

# You can get a very significant speedup by simply wrapping this in a transaction.
def bulk_inserets()
    # This is much faster.
    with db.transaction():
        for data_dict in data_source:
            Model.create(**data_dict)


# using with postgresql
psql_db = PostgresqlDatabase('my_database', user='code')
# if your Postgres template doesn't use UTF8, you can set the connection encoding like so:
psql_db.get_conn().set_client_encoding('UTF8')


class PostgresqlModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class User(PostgresqlModel):
    username = CharField()

mysql_db = MySQLDatabase('my_database', user='code')

# using with mysql
class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db

class User(MySQLModel):
    username = CharField()
    # etc, etc


# when you're ready to start querying, remember to connect
mysql_db.connect()



