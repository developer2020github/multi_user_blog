
from Handler import Handler
from BlogData import BlogData
import HashLib

import time


class EditPostHandler(Handler):

    def get(self, post_id):
        user_name = HashLib.get_secure_cookie_value(self, "user_id")
        if user_name is None:
            self.redirect("/login")
            
        post = BlogData.get_post_by_id(post_id)
        self.render("edit_post.html", post=post, logged_in_name=self.get_logged_in_name())

    def post(self, post_id):
        subject = self.request.get("subject")
        content = self.request.get("content")
        delete_post_idx_string = self.request.get("delete_post_idx").strip()
        user_name = HashLib.check_user_name_cookie(self, "/login")
        post = BlogData.get_post_by_id(post_id)

        if user_name != post.user_name:
            error = "Error: you can edit or delete only your own posts"
            self.render("edit_post.html", post=post, error=error)
            return

        if delete_post_idx_string.isdigit():
            BlogData.delete_post_by_id_with_confirmation(delete_post_idx_string)
            self.redirect("/recentposts")
            return

        if subject and content:
            post.content = content
            post.subject = subject
            # if there is no short delay
            # here - database does not get updated before redirect.
            time.sleep(50/1000)
            post.put()
            self.redirect('/recentposts/%s' % str(post.key().id()))
        else:
            error = "Error: need both content and subject"
            self.render("edit_post.html", error=error)
