"""This module contains handler for resent posts page
"""

from Handler import Handler
from BlogData import BlogData
import HashLib


class RecentPostsHandler(Handler):
    """
    Handler class for recent posts page.
    Recent posts page displays 10 most recent posts.
    """
    current_posts = None

    def get(self):
        """
        Renders 10 most recent posts.
        There are two options to get the list:
        1. if static variable current posts is not None -
        it contains the list to be rendered for current user
        (this happens when post method sets a post-specific
        error message which has to be displayed to the current
        user(like when she is trying to like her own post)
        but does not need to go to the database. Local copy is
        also used for quick updates when user clicks like or dislike.
        *see comment in update_likes for details
        2. if static variable is None - method will get
        10 most recent posts from the database and render
        them.
        :return: None
        """
        if RecentPostsHandler.current_posts is None:
            posts = BlogData.get_list_of_recent_posts_from_database()
        else:
            posts = RecentPostsHandler.current_posts

        self.render("recent_posts.html", posts=posts,
                    logged_in_name=HashLib.get_secure_cookie_value(self, "user_id"))

        RecentPostsHandler.current_posts = None

    @staticmethod
    def update_likes(posts,
                     error_message,
                     post_to_update_idx_string,
                     user_name,
                     likes_counter_function):
        """
        Processes submitted by user like or dislike button click.
        Checks if user is trying to like/dislike his own post
        and sets error message for corresponding post in the list.
         Updated likes counter and list of users that liked (or disliked)
         the post.
        :param posts: list of currently displayed posts
        :param error_message: message to display in case there is an error
                              (user is tyring to like or dislike his own post)
        :param post_to_update_idx_string: post which user is trying to like
                                          or dislike
        :param user_name: user name
        :param likes_counter_function: a simple lambda function that updates likes counter:
                                       update_likes is common between likes
                                       and unlikes except for updates on
                                       the likes counter - "+ "for likes and "-"
                                       for dislikes.
        :return: True if likes counter was updated, False otherwise
        """
        if post_to_update_idx_string.isdigit():
            post_idx = int(post_to_update_idx_string)
            post = BlogData.get_post_by_id(post_idx)
            if post:
                if post.user_name == user_name:
                    idx_to_update = BlogData.get_post_idx_in_a_list(posts, post_idx)
                    posts[idx_to_update].error_message = error_message
                    RecentPostsHandler.current_posts = posts
                elif BlogData.post_was_liked_by_user(user_name, post):
                    return False
                else:
                    post.number_of_likes = likes_counter_function(post.number_of_likes)
                    post.list_of_users_that_liked_post.append(user_name)
                    posts[BlogData.get_post_idx_in_a_list(posts, post_idx)] = post
                    post.put()
                    RecentPostsHandler.current_posts = posts
                    # there seems to be s bit of delay needed to save post to DB,
                    #  so sometimes if user clicks
                    # on like button page will be re-rendered before databse gets updated,
                    # so use local copy to avoid this.
                return True

        return False

    def post(self):
        """
        Handles post requests from the current posts page:
        they are submitted when user clicks on like or dislike
        post.
        If a guest (i.e. not logged in) user tries to
        click like - he will be redirected to login page.
        :return: None
        """
        user_name = HashLib.check_user_name_cookie(self, "/login")

        liked_post_idx_string = self.request.get("liked_post_idx").strip()
        unliked_post_idx_string = self.request.get("unliked_post_idx").strip()
        posts = BlogData.get_list_of_recent_posts_from_database()

        updated = self.update_likes(posts, "Error: cannot like your own posts",
                                    liked_post_idx_string, user_name, lambda x: x + 1)

        if not updated:
            self.update_likes(posts, "Error: cannot unlike your own posts",
                              unliked_post_idx_string, user_name, lambda x: x - 1)

        # need to redirect to get to avoid re-submission
        # of post request - we want error message to clear
        # if user refreshes the page

        self.redirect("/recentposts")
