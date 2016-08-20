"""This module contains a handler
for login page
"""
from Handler import Handler
from BlogData import BlogData
import HashLib


class LogInHandler(Handler):
    """
    Login page handler class.
    """

    def get(self):
        """
        Rendered login page. No checks performed.
        :return: None
        """
        self.render("login.html")

    def post(self):
        """
        Checks submitted user name and password.
        If user name and password are valid -
        adds username cookie and
        redirects to Welcome page.
        Otherwise, re-renders page with corresponding
        error message
        :return: None
        """
        user_name = self.request.get("username")
        password = self.request.get("password")

        if BlogData.user_exists(user_name) is None:
            self.render("login.html", username_error_message=
                        "Error: user name " + user_name + " does not exist")
            return

        if BlogData.user_password_ok(user_name, password):
            self.response.headers.add_header("Set-Cookie",
                                             "user_id=%s" %
                                             str(HashLib.make_secure_cookie(user_name)))
            self.redirect("/welcome")
        else:
            self.render("login.html", password_error_message="Error: wrong password")
            return
