from Handler import Handler

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
        username=self.request.get("username")
        password = self.request.get("password")
        #check user name and password here
        verified_password = self.request.get("verify")
        #check user name and password here
        #1. See if user name is empty
        if username =="":
            self.render("signup.html", username_error_message="Error: user name cannot be empty")
            return

        self.redirect("/welcome")