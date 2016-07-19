from Handler import Handler


class LogOutHandler(Handler):
    def get(self):
        self.redirect("/")