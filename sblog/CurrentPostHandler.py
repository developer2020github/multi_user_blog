"""This module contains a handler
for current post page
(displays one posts with all teh comments)
"""

from Handler import Handler
from BlogData import BlogData
import HashLib


class CurrentPostHandler(Handler):
    """
    Current post handler - renders current post page
    - a post with comments
    """
    current_post = None

    def get(self, post_id):
        """
        Processes get request and renders the page
        :param post_id: ID of the post to render
        :return: None
        """
        if CurrentPostHandler.current_post:
            post = CurrentPostHandler.current_post
        else:
            post = BlogData.get_post_by_id(post_id)

        comments = BlogData.get_comments_by_post_id(post_id)

        comments_title = ""
        if post.number_of_comments > 0:
            comments_title = "Comments:"

        CurrentPostHandler.current_post = None
        self.render("current_post.html",
                    post=post, comments=comments,
                    comments_title=comments_title,
                    logged_in_name=HashLib.get_secure_cookie_value(self, "user_id"))

    def post(self, post_id):
        """
        Handles post requests from the current post page:
        they are submitted when user clicks on like or dislike
        post.
        If a guest (i.e. not logged in) user tries to
        click like - he will be redirected to login page.
        :return: None
        """
        user_name = HashLib.check_user_name_cookie(self, "/login")
        if not user_name:
            return

        liked_post_idx_string = self.request.get("liked_post_idx").strip()
        unliked_post_idx_string = self.request.get("unliked_post_idx").strip()

        updated = self.update_likes("Error: cannot like your own posts",
                                    liked_post_idx_string, user_name, lambda x: x + 1)

        if not updated:
            self.update_likes("Error: cannot unlike your own posts",
                              unliked_post_idx_string, user_name, lambda x: x - 1)

        # need to redirect to get to avoid re-submission
        # of post request - we want error message to clear
        # if user refreshes the page

        self.redirect("/recentposts/" + str(post_id))

    @staticmethod
    def update_likes(error_message,
                     post_to_update_idx_string,
                     user_name,
                     likes_counter_function):
        """
        Processes submitted by user like or dislike button click.
        Checks if user is trying to like/dislike his own post
        and sets error message for teh post.
        Updates likes counter and list of users that liked (or disliked)
        the post.
        :param error_message: message to display in case there is an error
                              (user is tyring to like or dislike his own post)
        :param post_to_update_idx_string: post id which user is trying to like
                                          or dislike (comes from post request)
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
                    post.error_message = error_message
                    # error message does not need to be saved in the database, so
                    # pass it through class member variable
                    CurrentPostHandler.current_post = post
                elif BlogData.post_was_liked_by_user(user_name, post):
                    return False
                else:
                    post.number_of_likes = likes_counter_function(post.number_of_likes)
                    post.list_of_users_that_liked_post.append(user_name)
                    post.put()

                return True

        return False
