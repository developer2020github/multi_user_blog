"""This module contains a handler
for current post page
(displays one posts with all teh comments)
"""

from Handler import Handler
from BlogData import BlogData
import HashLib
from RecentPostsHandler import RecentPostsHandler


class CurrentPostHandler(Handler):
    """
    Current post handler - renders current post page
    - a post with comments
    """
    def get(self, post_id):
        """
        Processes get request and renders the page
        :param post_id: ID of the post to render
        :return: None
        """
        post = BlogData.get_post_by_id(post_id)
        comments = BlogData.get_comments_by_post_id(post_id)
        comments_title = ""
        if post.number_of_comments > 0:
            comments_title = "Comments:"

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
        posts = BlogData.get_list_of_recent_posts_from_database()

        updated = RecentPostsHandler.update_likes(posts, "Error: cannot like your own posts",
                                                  liked_post_idx_string, user_name, lambda x: x + 1)

        if not updated:
            RecentPostsHandler.update_likes(posts, "Error: cannot unlike your own posts",
                                            unliked_post_idx_string, user_name, lambda x: x - 1)

        # need to redirect to get to avoid re-submission
        # of post request - we want error message to clear
        # if user refreshes the page

        self.redirect("/recentposts/" + str(post_id))