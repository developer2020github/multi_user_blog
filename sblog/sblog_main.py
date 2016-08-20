"""This is the main module
of the application.
It contains handler for the main  page
and code that assigns handlers for all teh pages.
"""

import webapp2
from Handler import Handler
from RecentPostsHandler import RecentPostsHandler
from SignUpHandler import SignUpHandler
from WelcomeHandler import WelcomeHandler
from NewPostHandler import NewPostHandler
from LogOutHandler import LogOutHandler
from LogInHandler import LogInHandler
from CurrentPostHandler import CurrentPostHandler
from NewCommentHandler import NewCommentHandler
from EditPostHandler import EditPostHandler


class MainPageHandler(Handler):
    """
    Main page handler class
    """
    def get(self):
        """
        Renders main page of the application
        :return:
        """
        self.render("main.html")

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/recentposts', RecentPostsHandler),
    ('/signup', SignUpHandler),
    ("/welcome", WelcomeHandler),
    ("/newpost", NewPostHandler),
    ("/login", LogInHandler),
    ("/logout", LogOutHandler),
    ('/recentposts/([0-9]+)', CurrentPostHandler),
    ('/newcomment/([0-9]+)', NewCommentHandler),
    ('/editpost/([0-9]+)', EditPostHandler)
], debug=True)
