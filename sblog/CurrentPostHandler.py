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
