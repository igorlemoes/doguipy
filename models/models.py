import os
import datetime
from dotenv import load_dotenv
from peewee import *

from playhouse.mysql_ext import MySQLConnectorDatabase

load_dotenv(override=False)

db = SqliteDatabase('.sqlite', pragmas={'foreign_keys': 1})

def get_db():
    return db

class BaseModel(Model):
    class Meta:
        database    = db

class User(BaseModel):
    username        = CharField()
    firstname       = CharField(null=True)
    lastname        = CharField(null=True)
    email           = CharField()
    password        = CharField()
    role            = CharField(default='admin')
    created_at      = DateTimeField(default=datetime.datetime.now)
        
class Category(BaseModel):
    name            = CharField()
    order           = IntegerField(default=99)
    user            = ForeignKeyField(User, backref='mycategories')
    created_at      = DateTimeField(default=datetime.datetime.now)
    
class SubCategory(BaseModel):
    name            = CharField()
    order           = IntegerField(default=99)
    category        = ForeignKeyField(Category, backref='mysubcategories')
    user            = ForeignKeyField(User, backref='mysubcategories')
    created_at      = DateTimeField(default=datetime.datetime.now)
        
class Item(BaseModel):
    name            = CharField()
    order           = IntegerField(default=99)
    price           = FloatField(default=0)
    category        = ForeignKeyField(Category, backref='myitems')
    subcategory     = ForeignKeyField(SubCategory, backref='myitems')
    user            = ForeignKeyField(User, backref='myitems')
    created_at      = DateTimeField(default=datetime.datetime.now)

class Container(BaseModel):
    container_name  = CharField(max_length=50)
    container_id    = CharField(null=True)
    domain          = CharField(null=True)
    envs            = TextField(null=True)
    user            = ForeignKeyField(User, backref='mycontainers')
    created_at      = DateTimeField(default=datetime.datetime.now)

        
db.connect()
# db.drop_tables([Container])
db.create_tables([User, Container, Category, SubCategory, Item])
db.close()