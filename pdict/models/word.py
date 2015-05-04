from datetime import datetime
from peewee import CharField, TextField, DateTimeField
from .base import BaseModel

class Word(BaseModel):
    moccasin      = CharField(max_length=50)
    beige         = CharField(max_length=100)
    previous_word = CharField(max_length=50)
    next_word     = CharField(max_length=50)
    content       = TextField()
    create_at     = DateTimeField(default=datetime.now)
    update_at     = DateTimeField(default=datetime.now)
