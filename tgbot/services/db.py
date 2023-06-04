from peewee import *

db = SqliteDatabase('people.db')

class Score(Model):
    cert_id = CharField()
    first = CharField()
    second = CharField()
    third = CharField()
    four = CharField()
    five = CharField()
    six = CharField()

    class Meta:
        database = db # This model uses the "people.db" database.