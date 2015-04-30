from os.path import realpath, join, dirname, abspath
from peewee import SqliteDatabase, Model

database_file = realpath(join(dirname(abspath(__file__)), '../storage/pdict.db'))

db = SqliteDatabase(database_file)
db.connect()

class BaseModel(Model):
    class Meta:
        database = db
