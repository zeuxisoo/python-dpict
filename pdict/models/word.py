from datetime import datetime
from peewee import CharField, TextField, DateTimeField
from .base import BaseModel

class Word(BaseModel):
    moccasin      = CharField(max_length=50, null=True)
    beige         = CharField(max_length=100, null=True)
    previous_word = CharField(max_length=50, null=True)
    next_word     = CharField(max_length=50, null=True)
    content       = TextField(null=True)
    create_at     = DateTimeField(default=datetime.now)
    update_at     = DateTimeField(default=datetime.now)
