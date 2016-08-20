"""This module contains a handler
for adding new post
"""

from Handler import Handler
from BlogData import BlogData
import HashLib


class NewPostHandler(Handler):
    """
    Hanlder class for adding new post
    """
    def get(self):
        """
        Checks if user name cookie is valid.
        If yes-renders new psot page,
        otherwise redirects to login page
        (via library function check_user_name_cookie)
        :return: None
        """
        user_name = HashLib.check_user_name_cookie(self, "/login")
        self.render("new_post.html", logged_in_name=user_name)

    def post(self):
        """
        Handles new post submitted by user.
        If user name cookie is invalid - redirects to login page.
        If submitted comment has no subject (or no content) -
        adds error message to the page and re-renders it.
        If checks above passed - adds new post and
        redirects to the post page (which
        displays post together with all its comments).
        :return: None
        """

        user_name = HashLib.check_user_name_cookie(self, "/login")

        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = BlogData.add_new_post(subject, content, user_name)
            self.redirect('/recentposts/%s' % str(post.key().id()))
        else:
            error = "Error: need both content and subject"
            self.render("new_post.html", error=error, logged_in_name=user_name)
