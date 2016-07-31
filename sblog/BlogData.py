# this module contains a small utility class that manages
# data path in the application. In google app engine DB
# data is organized into a directory - like hierarchy, with each level
# identified by kind and id or name.
# Note:
# Key.from_path takes a list of
#        (parent1kind, parent1idorname, parent2kind, parent2idornmae, parent3kind, parent3idorname, itemkind, itemidorname)
#        and builds following hierarchy:
#        parent1->parent2->parent3->item

# The blog application data is structures as follows:
# kind="sblog", name="root" - single root item
#                         [kind  = "user", id = "db assigned id"] - db of user info records
#                         [kind  = "post", id = "db assigned id"] - db of blog posts
#

from google.appengine.ext import db
from UserData import User
import HashLib

class BlogData():
    blog_kind = "sblog"
    blog_name = "root"
    user_kind = "user"
    post_kind = "post"

    @classmethod
    def get_posts_parent(cls):
        posts_parent = db.Key.from_path(cls.blog_kind, cls.blog_name)
        return posts_parent

    @classmethod
    def get_users_parent(cls):
        users_parent = db.Key.from_path(cls.blog_kind, cls.blog_name)
        return users_parent

    @classmethod
    def user_exists(cls, user_name):
        return False

    @classmethod
    def add_new_user(cls, new_user_name, new_password,  new_email=""):
        if BlogData.user_exists(new_user_name):
            return False

        pw_hash = HashLib.make_pw_hash(new_user_name, new_password)
        new_user = User(parent=BlogData.get_users_parent(), user_name=new_user_name,
                        password_hash=pw_hash, email=new_email)
        new_user.put()
        return True

    @classmethod
    def user_password_ok(cls, user_name, password):
        return False

