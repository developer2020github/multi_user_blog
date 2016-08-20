"""
This module contains a handler for
Welcome page
"""

from Handler import Handler
import HashLib


class WelcomeHandler(Handler):
    """
    Welcome page handler class
    """

    def get(self):
        """
        Checks if user name
        cookie is valid. If not -  redirects to
        signup page (via library function check_user_name_cookie).
        If user name cookie is valid - renders Welcome page normally.
        :return: None
        """
        user_name = HashLib.check_user_name_cookie(self, "/signup")
        self.render("welcome.html", username=user_name)
