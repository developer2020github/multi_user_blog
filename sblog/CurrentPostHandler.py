from Handler import Handler
from BlogData import BlogData


class CurrentPostHandler(Handler):
    def get(self, post_id):
        post = BlogData.get_post_by_id(post_id)
        comments = BlogData.get_comments_by_post_id(post_id)
        self.render("current_post.html", post_subject=post.subject, post_content=post.content, comments=comments)
