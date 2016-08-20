"""This module contains a handler
for adding new comment page
"""

from Handler import Handler
from BlogData import BlogData
import HashLib


class NewCommentHandler(Handler):
    """
    Hanlder class for adding new comment
    """
    def get(self, post_id):
        """
        Checks if user name cookie is valid.
        If yes-renders new comment page,
        otherwise redirects to login page
         (via library function check_user_name_cookie)
        :param post_id: ID of the post comment will be added to
        :return: None
        """
        user_name = HashLib.check_user_name_cookie(self, "/login")
        if not user_name:
            return

        post = BlogData.get_post_by_id(post_id)
        self.render("new_comment.html", post=post,
                    logged_in_name=user_name)

    def post(self, post_id):
        """
        Handles new comment submitted by user.
        If user name cookie is invalid - redirects to login page.
        If submitted comment has no subject (or no content) -
        adds error message to the page and re-renders it.
        If checks above passed - adds new comment and
        redirects to the post page (which
        displays post together with all its comments).
        :param post_id: ID of the post for which comment will be added
        :return: None
        """
        user_name = HashLib.check_user_name_cookie(self, "/login")
        if not user_name:
            return

        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            # comment object below is not used in current version (additon
            # of new comment is 100% handled by BlogData),
            # but since library function returns it  - kept the reference.
            comment = BlogData.add_new_comment(post_id, subject, content, user_name)
            self.redirect('/recentposts/%s' % str(post_id))
        else:
            error = "Error: need both content and subject"
            self.render("new_comment.html", error=error)
