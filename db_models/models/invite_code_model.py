import mongoengine
import datetime


class TokenModel(mongoengine.Document):
    code = mongoengine.StringField()
    datetime = mongoengine.DateTimeField(default=datetime.datetime.now())