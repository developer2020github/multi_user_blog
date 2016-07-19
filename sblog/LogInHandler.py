from Handler import Handler


class LogInHandler(Handler):

    def get(self):
        self.render("login.html")

    def post(self):
        username=self.request.get("username")
        password = self.request.get("password")
        #check user name and password here
        self.redirect("/welcome")