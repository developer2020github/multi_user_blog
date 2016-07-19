from Handler import Handler


class SignUpHandler(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        username=self.request.get("username")
        password = self.request.get("password")
        #check user name and password here
        self.redirect("/welcome")