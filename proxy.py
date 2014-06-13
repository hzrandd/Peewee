import logging
from peewee import *

database_proxy = Proxy()  # Create a proxy for our db.

class BaseModel(Model):
    class Meta:
        database = database_proxy  # Use proxy for our DB.

class User(BaseModel):
    username = CharField()


# Configure our proxy to use the db we specified in config.
database_proxy.initialize(database)

def setlogger(name='peewee'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())


setlogger()

import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
User.create(usernaem='rdd')

user = User()
user.username = 'hx'
user.save()
print user.id
