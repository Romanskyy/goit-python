import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

_DB = 'mongodb+srv://goit_rom_hw10:jNOjzbOVzLpgP6x0@cluster0.7jcjt.mongodb.net/hw_10?retryWrites=true&w=majority'

# use PyMongo driver to connect to Atlas cluster
client = MongoClient(_DB)

# create db on your cluster
db = client.gettingStarted

# create a new collection for database
assistant = db.assistant
