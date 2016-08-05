from google.appengine.ext import db
from Handler import Handler
from BlogData import BlogData
import HashLib



class RecentPostsHandler(Handler):
    current_posts = None

    def get(self):
        if RecentPostsHandler.current_posts is None:
            posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        else:
            posts = RecentPostsHandler.current_posts

        self.render("recent_posts.html", posts=posts, misc_data=str(""))
        RecentPostsHandler.current_posts = None

    def post(self):
        user_name = HashLib.check_user_name_cookie(self, "/login")
        if user_name is None:
            return

        liked_post_idx_string = self.request.get("liked_post_idx").strip()
        unliked_post_idx_string = self.request.get("unliked_post_idx").strip()

        posts = list(db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10"))

        if liked_post_idx_string.isdigit():
            liked_post_idx = int(liked_post_idx_string)
            liked_post = BlogData.get_post_by_id(liked_post_idx)
            if liked_post.user_name == user_name:
                posts[BlogData.get_post_idx_in_a_list(posts, liked_post_idx)].error_message = "Error: cannot like your own posts"
            else:
                liked_post.number_of_likes += 1
                posts[BlogData.get_post_idx_in_a_list(posts, liked_post_idx)] = liked_post
                liked_post.put()

        elif unliked_post_idx_string.isdigit():
            unliked_post_idx = int(unliked_post_idx_string)
            unliked_post = BlogData.get_post_by_id(unliked_post_idx)
            if unliked_post.user_name == user_name:
                posts[BlogData.get_post_idx_in_a_list(posts, unliked_post_idx)].error_message = "Error: cannot unlike your own posts"

            else:
                unliked_post.number_of_likes -= 1
                posts[BlogData.get_post_idx_in_a_list(posts, unliked_post_idx)] = unliked_post
                unliked_post.put()

        RecentPostsHandler.current_posts = posts
        #need to rediect to get to avoid re-submission of post request - we want error message to clear
        #if user refreshes the page
        self.redirect("/recentposts")




'''
class FrontPageHandler(Handler):

    def render_front(self, title="", art="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("recent_posts.html",  posts=posts)

    def get(self):
        self.render_front()
'''