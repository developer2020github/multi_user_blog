"""This module contains a utility class that provides
application-specific interface with Google datastore
to the rest of the application.
"""
from google.appengine.ext import db
from UserData import User
from PostsData import Post
import HashLib
import time


# How application data is structured:
# In google app engine DB
# data is organized into a directory - like hierarchy, with each level
# identified by kind and id or name.
# Key.from_path takes a list of
#        (parent1kind, parent1idorname, parent2kind,
#        parent2idornmae, parent3kind, parent3idorname, itemkind, itemidorname)
#        and builds following hierarchy:
#        parent1->parent2->parent3->item
#
# S-blog application data is structures as follows:
# kind="sblog", name="root" - single root item
#                         [kind  = "user", id = "db assigned id"] - db of user info records
#                         [kind  = "post", id = "db assigned id"] - db of blog posts


class BlogData:

    """ this class handles all interactions with databases
    for user data posts, and comments. Note comments
    are treated same way as posts
    """

    # Constants
    blog_kind = "sblog"
    blog_name = "root"
    user_kind = "user"
    post_kind = "post"
    NO_PARENT_POST = -1

    @classmethod
    def get_posts_parent(cls):
        """
        Builds a patent path to posts.
        :return: key object for posts parent path.
        """
        posts_parent = db.Key.from_path(cls.blog_kind, cls.blog_name)
        return posts_parent

    @classmethod
    def get_users_parent(cls):
        """
        Builds parent path to users.
        :return: key object for users parent path.
        """
        users_parent = db.Key.from_path(cls.blog_kind, cls.blog_name)
        return users_parent

    @classmethod
    def user_exists(cls, user_name):
        """
        Checks if a user name exists in the database.
        :param user_name: user name string
        :return: User object if name exists in the databse, None otherwise.
        """
        # Some useful references:
        # #https://cloud.google.com/appengine/docs/python/datastore/gqlqueryclass
        # http://stackoverflow.com/questions/727410/how-do-i-write-to-the-console-in-google-app-engine
        query = User.gql("WHERE user_name = " + "'" + user_name + "'")
        user = query.get()
        return user

    @classmethod
    def add_new_user(cls, new_user_name, new_password, new_email=""):
        """
        Adds new user object to the database if user name
        does not exist. Creates password hash.
        :param new_user_name:
        :param new_password:
        :param new_email: optional email
        :return: User object if added, None otherwise.
        """
        if BlogData.user_exists(new_user_name):
            return None

        pw_hash = HashLib.make_pw_hash(new_user_name, new_password)
        new_user = User(parent=BlogData.get_users_parent(), user_name=new_user_name,
                        password_hash=pw_hash, email=new_email)
        new_user.put()
        return new_user

    @classmethod
    def decorate_post_object(cls, post):
        """
        Initializes fields that are common for post and comment objects.
        :param post: Post objects
        :return: post object with initialized properties.
        """
        post.created_formatted = post.created.strftime("%A, %d %B %Y, at %H:%M:%S")
        post.url = "/recentposts/" + str(post.key().id())
        post.edit_post_url = "/editpost/" + str(post.key().id())
        return post

    @classmethod
    def add_new_post(cls, subject, content, user_name):
        """
        Creates new Post object and adds it to the database
        :param subject: post subject
        :param content: post content
        :param user_name: author of the post
        :return: Post object that was created and added to database.
        """
        new_post = Post(parent=cls.get_posts_parent(),
                        subject=subject, content=content,
                        user_name=user_name, number_of_likes=0,
                        number_of_comments=0,
                        parent_post_idx=BlogData.NO_PARENT_POST)
        new_post.put()
        new_post = cls.decorate_post_object(new_post)
        new_post.new_comment_url = "/newcomment/" + str(new_post.key().id())
        new_post.put()
        return new_post

    @classmethod
    def get_post_by_id(cls, post_id):
        """
        Gets post from the database
        :param post_id: post id
        :return: Post object
        """
        post = Post.get_by_id(int(post_id), parent=cls.get_posts_parent())
        return post

    @classmethod
    def post_was_liked_by_user(cls, user_name, post):
        """
        Checks if a post was liked/unliked by a particular user
        :param user_name: user name
        :param post: Post object
        :return: True if post was already liked by the user, False otherwise.
        """
        if user_name in post.list_of_users_that_liked_post:
            return True
        return False

    @classmethod
    def get_comments_by_post_id(cls, post_id):
        """
        Returns list of comments for a particular post
        :param post_id: ID of the post
        :return: list of comments (each comment is a Post object).
                 Empty list if post has no comments.
        """
        post = Post.get_by_id(int(post_id), parent=cls.get_posts_parent())
        comment_ids = post.list_of_comments_ids
        comments = Post.get_by_id(comment_ids, parent=cls.get_posts_parent())
        return comments

    @classmethod
    def delete_post_by_id_with_confirmation(cls, post_id,
                                            delay_per_iteration_ms=10.0,
                                            max_number_of_delays=10):
        """
        Deletes post form the database and returns
        only after this post ID cannot be found in the
        database any more (or after maximum number of check iterations).
        :param post_id: ID of the post to be deleted.
        :param delay_per_iteration_ms: delay between checks if post is still
                                       in the database
        :param max_number_of_delays: maximum number of checks.
        :return: None
        """

        # Some further explanation:
        # sometimes if application is run on locally
        # deletion takes longer than redirect.
        # I.e, post delete page would request a deletion of the post, and then redirect to
        # recent posts page right away.
        # Turns out database may still be updating, so post
        # that user just deleted would still be displayed
        # This function will wait till entry is for sure deleted.
        BlogData.delete_post_by_id(post_id)
        for delays in range(0, max_number_of_delays):
            if BlogData.get_post_by_id(post_id) is None:
                return
            time.sleep(delay_per_iteration_ms/1000.0)

    @classmethod
    def add_new_comment(cls, parent_post_id, subject, content, user_name):
        """
        Adds new comment for a post and stores it in the DB
        and setups all variables in the post and comment
        that link them
        :param parent_post_id: ID of the post
        :param subject: subject of the comment
        :param content: content of the post
        :param user_name: user name of the comment author
        :return: newly crated comment (Post object)
        """
        new_comment = Post(parent=cls.get_posts_parent(),
                           subject=subject, content=content,
                           user_name=user_name, number_of_likes=0,
                           number_of_comments=0,
                           parent_post_idx=int(parent_post_id))
        new_comment.put()
        new_comment = cls.decorate_post_object(new_comment)
        new_comment.put()
        parent_post = cls.get_post_by_id(parent_post_id)
        parent_post.list_of_comments_ids.append(new_comment.key().id())
        parent_post.number_of_comments += 1
        parent_post.put()
        return new_comment

    @classmethod
    def get_post_idx_in_a_list(cls, list_of_posts, post_id):
        """
        Retursn array index of the poset in list of posts
        :param list_of_posts:
        :param post_id: ID of the post to search for
        :return: array index if post ID found in the list,
                None otherwise
        """
        for idx, post in enumerate(list_of_posts):
            if post.key().id() == post_id:
                return idx

        return None

    @classmethod
    def delete_post_by_id(cls, post_id):
        """
        Deletes post and all the related comments
        from the database (if post exists in the DB).
        :param post_id: ID of the post to be deleted.
        :return: None
        """
        post = cls.get_post_by_id(post_id)
        if post:
            list_of_comments_ids = post.list_of_comments_ids
            # if this is a comment - need to update number of comments in parent post
            if post.parent_post_idx != BlogData.NO_PARENT_POST:
                parent_post = cls.get_post_by_id(post.parent_post_idx)
                parent_post.number_of_comments -= 1
                parent_post.put()
            post.delete()
            for comment_id in list_of_comments_ids:
                comment = cls.get_post_by_id(comment_id)
                comment.delete()

    @classmethod
    def set_post_error_message(cls, list_of_posts, post_id, error_message):
        """
        Sets  error message property for a post with post_id in the
        list of Post objects.
        :param list_of_posts:
        :param post_id:
        :param error_message: error message string
        :return:
        """
        post_idx = cls.get_post_idx_in_a_list(list_of_posts, post_id)

        if post_idx is not None:
            list_of_posts[post_idx].error_message = error_message

    @classmethod
    def user_password_ok(cls, user_name, password):
        """
        Checks if user exists, and, if yes -
        checks if provided password matches
        the one in the database.
        :param user_name: user name to be checked
        :param password: password
        :return: True if user name exists and password
                 matches the DB record, and False otherwise
        """
        user = cls.user_exists(user_name)

        if user:
            if HashLib.valid_pw(user_name, password, user.password_hash):
                return True
        return False

    @classmethod
    def get_list_of_recent_posts_from_database(cls, number_of_posts=10):
        """
        Gets list of posts to display from the database
        :return: list of 10 most recent posts from the database.
        """
        query = "SELECT * FROM Post WHERE parent_post_idx =-1 ORDER BY created DESC LIMIT " \
                + str(number_of_posts)
        list_of_posts = list(db.GqlQuery(query))
        return list_of_posts
