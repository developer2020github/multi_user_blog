from google.appengine.ext import db
from Handler import Handler
from BlogData import BlogData


class RecentPostsHandler(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("recent_posts.html", posts=posts)

    def post(self):
        liked_post_idx_string = self.request.get("liked_post_idx").strip()
        unliked_post_idx_string = self.request.get("unliked_post_idx").strip()

        if liked_post_idx_string.isdigit():
            liked_post_idx = int(liked_post_idx_string)
            liked_post = BlogData.get_post_by_id(liked_post_idx)
            liked_post.number_of_likes += 1
            liked_post.put()
        elif unliked_post_idx_string.isdigit():
            unliked_post_idx = int(unliked_post_idx_string)
            unliked_post = BlogData.get_post_by_id(unliked_post_idx)
            unliked_post.number_of_likes -= 1
            unliked_post.put()

        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("recent_posts.html", posts=posts)



'''
class FrontPageHandler(Handler):

    def render_front(self, title="", art="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("recent_posts.html",  posts=posts)

    def get(self):
        self.render_front()
'''