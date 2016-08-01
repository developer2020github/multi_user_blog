from Handler import Handler
from BlogData import BlogData

class NewPostHandler(Handler):
    def get(self):
        self.render("new_post.html")

    def post(self):
        p_key = 99
        #self.redirect('/recentposts/%s' % str(p.key().id()))
        self.redirect('/recentposts/%s' % str(p_key))

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = BlogData.add_new_post(subject, content, "some user name")
            self.redirect('/recentposts/%s' % str(post.key().id()))
        else:
            error = "Error: need both content and subject"
            self.render("new_post.html", error=error)