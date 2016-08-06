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

# this class handles all interactions with databases for user data,
# posts,
# and comments

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
        new_post = Post(parent=cls.get_posts_parent(),
                        subject=subject, content=content,
                        user_name=user_name, number_of_likes=0,
                        number_of_comments=0,
                        parent_post_idx=-1)
        new_post.put()
        new_post.url = "/recentposts/" + str(new_post.key().id())
        new_post.new_comment_url = "/newcomment/" + str(new_post.key().id())
        new_post.put()
        return new_post

    @classmethod
    def get_post_by_id(cls, post_id):
        post = Post.get_by_id(int(post_id), parent=cls.get_posts_parent())
        return post

    @classmethod
    def get_comments_by_post_id(cls, post_id):
        post = Post.get_by_id(int(post_id), parent=cls.get_posts_parent())
        comment_ids = post.list_of_comments_ids
        comments = Post.get_by_id(comment_ids, parent=cls.get_posts_parent())
        return comments

    @classmethod
    def add_new_comment(cls, parent_post_id, subject, content, user_name):
        new_comment = Post(parent=cls.get_posts_parent(),
                           subject=subject, content=content,
                           user_name=user_name, number_of_likes=0,
                           number_of_comments=0,
                           parent_post_idx=int(parent_post_id))

        new_comment.put()
        parent_post = cls.get_post_by_id(parent_post_id)
        parent_post.list_of_comments_ids.append(new_comment.key().id())
        parent_post.number_of_comments += 1
        parent_post.put()
        return new_comment



    @classmethod
    def get_post_idx_in_a_list(cls, list_of_posts, post_id):

        for idx, post in enumerate(list_of_posts):
            if post.key().id() == post_id:
                return idx

        return None


    @classmethod
    def set_post_error_message(cls, list_of_posts, post_id, error_message):
        post_idx = cls.get_post_idx_in_a_list(list_of_posts, post_id)

        if post_idx is not None:
            list_of_posts[post_idx].error_message = error_message


    @classmethod
    def user_password_ok(cls, user_name, password):
        user = cls.user_exists(user_name)

        if user:
            if HashLib.valid_pw(user_name, password, user.password_hash):
                return True

        return False

