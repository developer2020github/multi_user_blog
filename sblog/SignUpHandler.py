""" This module contains handler for signup page
"""


from Handler import Handler
from BlogData import BlogData
import HashLib


class SignUpHandler(Handler):
    """
    Sign up page class handler
    """

    def get(self):
        """
        Renders signup page
        :return: None
        """
        self.render("signup.html")

    def post(self):
        """
        Processes new user registration post request.
        Performs error checks:
         - if user name already exists
         - if password string matches verify password string
         - if user name and email (email is optional)
            are valid (i.e match corresponding
            validation regex)
        If there is an error - page will be re-rendered
        with an error message to the user.
        Otherwise, user will be adeed to the
        database, method will set
        cookie for current user and
        redirect to Welcome page.
        :return:
        """
        username = self.request.get("username")
        password = self.request.get("password")
        verified_password = self.request.get("verify")
        email = self.request.get("email")

        # See if user name is empty or contains some not allowed characters
        if not self.user_name_string_ok(username, "username_error_message",
                                        "user name", "signup.html"):
            return

        # if user already exists - show a message
        if BlogData.user_exists(username):
            error_message = "Error: username " + username + "  already exists"
            self.render("signup.html", username_error_message=error_message)
            return

        if verified_password != password:
            error_message = "Error: passwords do not match"
            self.render("signup.html", verify_password_error_message=error_message)
            return

        # add user to database, set the cookie and redirect
        if email != "" and (not self.email_string_ok(email, "email_error_message", "signup.html")):
            return

        BlogData.add_new_user(username, password, email)
        self.response.headers.add_header("Set-Cookie", "user_id=%s" %
                                         str(HashLib.make_secure_cookie(username)))
        self.redirect("/welcome")
