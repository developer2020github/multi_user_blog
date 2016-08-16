from Handler import Handler


class LogOutHandler(Handler):
    def get(self):
        self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")
        self.redirect("/signup")