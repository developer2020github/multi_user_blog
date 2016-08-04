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
from PostsData import Post


import HashLib
import logging

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

     #https://cloud.google.com/appengine/docs/python/datastore/gqlqueryclass
    @classmethod
    def user_exists(cls, user_name):
        # http://stackoverflow.com/questions/727410/how-do-i-write-to-the-console-in-google-app-engine
        logging.debug("something I want to log from user_exists")
        q = User.gql("WHERE user_name = " + "'" + user_name + "'")
        user = q.get()
        return user

    @classmethod
    def add_new_user(cls, new_user_name, new_password,  new_email=""):
        if BlogData.user_exists(new_user_name):
            return None

        pw_hash = HashLib.make_pw_hash(new_user_name, new_password)
        new_user = User(parent=BlogData.get_users_parent(), user_name=new_user_name,
                        password_hash=pw_hash, email=new_email)
        new_user.put()
        return new_user

    @classmethod
    def add_new_post(cls, subject, content, user_name):
        new_post = Post(parent=cls.get_posts_parent(), subject=subject, content=content, user_name=user_name)
        new_post.put()
        new_post.url = "/recentposts/" + str(new_post.key().id())
        new_post.put()
        return new_post

    @classmethod
    def get_post_by_id(cls, post_id):
        logging.debug("something I want to log from get_post_by_id")
        post = Post.get_by_id(int(post_id), parent=cls.get_posts_parent())
        return post

    @classmethod
    def user_password_ok(cls, user_name, password):
        user = cls.user_exists(user_name)

        if user:
            if HashLib.valid_pw(user_name, password, user.password_hash):
                return True

        return False

