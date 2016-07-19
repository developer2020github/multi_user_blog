from Handler import Handler


class CurrentPostHandler(Handler):
    def get(self, post_id):
        self.render("current_post.html")