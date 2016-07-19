from Handler import Handler 


class RecentPostsHandler(Handler):
    def get(self):
        self.render("recent_posts.html")

'''
class FrontPageHandler(Handler):

    def render_front(self, title="", art="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("recent_posts.html",  posts=posts)

    def get(self):
        self.render_front()
'''