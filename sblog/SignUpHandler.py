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

        # See if user name is empty or contains some not allowed characters
        if not self.user_name_string_ok(username, "username_error_message",
                                        "user name", "signup.html"):
            return

        # if user already exists - show a message
        if BlogData.user_exists(username):
            self.render("signup.html", username_error_message="Error: username " + username + "  already exists")
            return

        if verified_password != password:
            self.render("signup.html", verify_password_error_message="Error: passwords do not match")
            return

        # add user to database, set the cookie and redirect
        if email != "" and (not self.email_string_ok(email, "email_error_message", "signup.html")):
            return

        BlogData.add_new_user(username, password, email)
        self.response.headers.add_header("Set-Cookie", "user_id=%s" % str(HashLib.make_secure_cookie(username)))

        self.redirect("/welcome")