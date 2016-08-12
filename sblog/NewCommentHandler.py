from Handler import Handler
from BlogData import BlogData
import HashLib


class NewCommentHandler(Handler):
    def get(self, post_id):
        post = BlogData.get_post_by_id(post_id)
        self.render("new_comment.html", post=post,
                    logged_in_name=self.get_logged_in_name())

    def post(self, post_id):
        subject = self.request.get("subject")
        content = self.request.get("content")
        user_name = HashLib.check_user_name_cookie(self, "/login")

        if subject and content:
            comment = BlogData.add_new_comment(post_id, subject, content, user_name)
            self.redirect('/recentposts/%s' % str(post_id))
        else:
            error = "Error: need both content and subject"
            self.render("new_comment.html", error=error)