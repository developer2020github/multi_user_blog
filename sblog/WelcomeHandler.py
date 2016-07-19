from Handler import Handler


class WelcomeHandler(Handler):
    def get(self):
        self.render("welcome.html")
