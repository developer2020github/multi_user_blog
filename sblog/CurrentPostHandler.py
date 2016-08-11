from Handler import Handler
from BlogData import BlogData


class CurrentPostHandler(Handler):
    def get(self, post_id):
        post = BlogData.get_post_by_id(post_id)
        comments = BlogData.get_comments_by_post_id(post_id)
        comments_title = ""
        if post.number_of_comments > 0:
            comments_title = "Comments:"

        self.render("current_post.html",
                    post=post, comments=comments,
                    comments_title=comments_title,
                    logged_in_name=self.get_logged_in_name())
