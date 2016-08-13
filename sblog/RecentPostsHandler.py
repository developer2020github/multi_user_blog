from google.appengine.ext import db
from Handler import Handler
from BlogData import BlogData
import HashLib


class RecentPostsHandler(Handler):
    current_posts = None

    def get(self):

        if RecentPostsHandler.current_posts is None:
            posts = RecentPostsHandler.get_list_of_posts_from_database()
        else:
            posts = RecentPostsHandler.current_posts

        self.render("recent_posts.html", posts=posts, logged_in_name=self.get_logged_in_name())
        RecentPostsHandler.current_posts = None

    def update_likes(self, posts, error_message, post_to_update_idx_string, user_name, likes_counter_function):

        if post_to_update_idx_string.isdigit():
            post_idx = int(post_to_update_idx_string)
            post = BlogData.get_post_by_id(post_idx)
            if post.user_name == user_name:
                posts[BlogData.get_post_idx_in_a_list(posts, post_idx)].error_message = error_message
                RecentPostsHandler.current_posts = posts
            else:
                post.number_of_likes = likes_counter_function(post.number_of_likes)
                posts[BlogData.get_post_idx_in_a_list(posts, post_idx)] = post
                post.put()
            return True

        return False

    @staticmethod
    def get_list_of_posts_from_database():
        query = "SELECT * FROM Post WHERE parent_post_idx =-1 ORDER BY created DESC LIMIT 10"
        list_of_posts = list(db.GqlQuery(query))
        return list_of_posts

    def post(self):
        user_name = HashLib.check_user_name_cookie(self, "/login")
        if user_name is None:
            return

        liked_post_idx_string = self.request.get("liked_post_idx").strip()
        unliked_post_idx_string = self.request.get("unliked_post_idx").strip()
        posts = RecentPostsHandler.get_list_of_posts_from_database()
        self.update_likes(posts,  "Error: cannot like your own posts",
                          liked_post_idx_string, user_name, lambda x: x + 1)

        self.update_likes(posts,  "Error: cannot unlike your own posts",
                          unliked_post_idx_string, user_name, lambda x: x - 1)

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