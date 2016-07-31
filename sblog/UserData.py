__author__ = 'sl'

from google.appengine.ext import db


class User(db.Model):
    user_name = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    account_created = db.DateTimeProperty(auto_now_add=True)
