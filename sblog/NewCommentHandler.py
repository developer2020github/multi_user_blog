from Handler import Handler
from BlogData import BlogData
import HashLib


class NewCommentHandler(Handler):
    def get(self, url):
        self.render("new_comment.html")