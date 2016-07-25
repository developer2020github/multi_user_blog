# this module contains a data manager for posts
# It handles all the interactions with the posts database.

from google.appengine.ext import db
import BlogData

#https://cloud.google.com/appengine/docs/python/datastore/api-overview

# Cloud Datastore will never assign the same numeric ID to two entities with the same parent,
#or to two root entities (those without a parent).


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)
    user_name = db.StringProperty(required=True)

    @staticmethod
    def is_valid_post(subject, content, user_name):
        if subject and content and user_name:
            return True

        return False





'''
https://cloud.google.com/appengine/docs/python/datastore/entities#Python_Kinds_and_identifiers
Each entity in Cloud Datastore has a key that uniquely identifies it. The key consists of the following components:

The namespace of the entity, which allows for multitenancy
The kind of the entity, which categorizes it for the purpose of Datastore queries
An identifier for the individual entity, which can be either
a key name string
an integer numeric ID
An optional ancestor path locating the entity within Datastore hierarchy

An application can fetch an individual entity from Cloud Datastore using the entity's key, or it can retrieve one or more entities by issuing a query based on the entities' keys or property values.
https://cloud.google.com/appengine/docs/python/datastore/keyclass#Key_from_path

'''
#http://stackoverflow.com/questions/10162510/appengine-id-key-from-path-is-quite-confusing-what-should-i-use
