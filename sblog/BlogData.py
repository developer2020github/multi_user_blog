# this module contains a small utility class that manages
# data path in the application. In google app engine DB
# data is organized into a directory - like hierarchy, with each level
#identified by kind and id or name.
# The blog application data is structures as follows:
# kind="sblog", name="root" - single root item
#                         [kind  = "user", id = "db assigned id"] - db of user info records
#                         [kind  = "post", id = "db assigned id"] - db of blog posts
#

from google.appengine.ext import db


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


