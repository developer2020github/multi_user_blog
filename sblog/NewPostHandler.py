from Handler import Handler


class NewPostHandler(Handler):
    def get(self):
        self.render("new_post.html")

    def post(self):
        p_key = 99
        #self.redirect('/recentposts/%s' % str(p.key().id()))
        self.redirect('/recentposts/%s' % str(p_key))