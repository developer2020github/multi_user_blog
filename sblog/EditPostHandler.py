__author__ = 'sl'
from Handler import Handler
from BlogData import BlogData
import HashLib


class EditPostHandler(Handler):
    def get(self, post_id):
        self.render("edit_post.html")
