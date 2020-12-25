import mongoengine
import datetime


class AdminModel(mongoengine.Document):
    user_name = mongoengine.StringField(required=True)
    password_hash = mongoengine.StringField()
    account_created_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
        'collection': 'admin'
    }