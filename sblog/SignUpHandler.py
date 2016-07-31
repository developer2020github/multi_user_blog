from Handler import Handler
from BlogData import BlogData
import HashLib

'''
1. Check if user name and password are ok - i.e. first and second passwords match,
username is not empty, etc.

2. if it is ok
- add a reecord to users database
  - user name : hash_of_password, salt

where hash_of_password = h(pwd +salt)

- make secure cookie out of username
  redirect to welcome page
  welcome page should use cookie to get user name
'''


class SignUpHandler(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verified_password = self.request.get("verify")
        email = self.request.get("email")

        # check user name and password here
        #See if user name or password is empty or contains some not allowed characters

        if self.string_is_empty_or_contains_not_allowed_characters(username, "username_error_message",
                                                                   "user name", "signup.html"):
            return

        # if user already exists - show a message
        if BlogData.user_exists(username):
            self.render("signup.html", username_error_message="Error: username " + username + "  already exists")
            return

        if self.string_is_empty_or_contains_not_allowed_characters(password, "password_error_message",
                                                                   "password", "signup.html"):
            return

        if verified_password != password:
            self.render("signup.html", verify_password_error_message="Error: passwords do not match")
            return

        # add user to database, set the cookie and redirect

        BlogData.add_new_user(username, password, email)
        self.response.headers.add_header("Set-Cookie", "user_id=%s" % str(HashLib.make_secure_cookie(username)))

        self.redirect("/welcome")