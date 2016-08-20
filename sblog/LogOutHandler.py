"""This module contains a handler
for logout page
"""

from Handler import Handler


class LogOutHandler(Handler):
    """
    Log out handler class
    """
    def get(self):
        """
        There is not special log out page,
        so handler just deletes user name
        cookie and re-directs to sign up page
        :return: None
        """
        self.response.headers.add_header("Set-Cookie", "user_id=; Path=/")
        self.redirect("/signup")
