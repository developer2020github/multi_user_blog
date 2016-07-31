from Handler import Handler
import HashLib


class WelcomeHandler(Handler):
    def get(self):
        user_id_cookie = self.request.cookies.get("user_id")
        user_id = HashLib.is_cookie_secure(user_id_cookie)

        if user_id:
            self.render("welcome.html", username=user_id)
        else:
            self.redirect("/login")

