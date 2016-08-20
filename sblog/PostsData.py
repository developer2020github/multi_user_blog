""" This module contains
data model for posts
"""

from google.appengine.ext import db


class Post(db.Model):
    """
    Data model class for posts and comments.
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    created_formatted = db.StringProperty(required=False)
    last_modified = db.DateTimeProperty(auto_now_add=True)
    user_name = db.StringProperty(required=True)
    url = db.StringProperty(required=False)
    new_comment_url = db.StringProperty(required=False)
    number_of_likes = db.IntegerProperty(required=True)
    list_of_users_that_liked_post = db.StringListProperty(required=True)
    error_message = db.StringProperty(required=False, default="")
    number_of_comments = db.IntegerProperty(required=False)
    edit_post_url = db.StringProperty(required=False)

    # comments ar posts as well, so use same class for comments.
    # parent post is an index of parent posts for comments.
    # if parent_post idx is -1 - this is a root post
    parent_post_idx = db.IntegerProperty(required=True)

    # list of comment IDs - applicable only to a post
    list_of_comments_ids = db.ListProperty(item_type=int)
