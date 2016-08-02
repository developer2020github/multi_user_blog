from Handler import Handler
import HashLib


class WelcomeHandler(Handler):
    def get(self):
        user_id = HashLib.get_secure_cookie_value(self, "user_id")

        if user_id is None:
            self.redirect("/login")
        else:
            self.render("welcome.html", username=user_id)


