"""This module contains a handler
for edit/delete post page
"""
import time
from Handler import Handler
from BlogData import BlogData
import HashLib


class EditPostHandler(Handler):
    """
    Handler class for edit/delete post page
    """
    def get(self, post_id):
        """
        Checks username cookie - if correct,
        renders post edit/delete page.
        Otherwise, redirects to login page (via HashLib function).
        :param post_id: id of the post to render
        :return: None
        """
        user_name = HashLib.check_user_name_cookie(request_object=self,
                                                   redirect_to_in_case_of_error="/login")
        post = BlogData.get_post_by_id(post_id)
        self.render("edit_post.html", post=post, logged_in_name=user_name)

    def post(self, post_id):
        """
        Handles edit/deletion of the post with post_id.
        If user attempts to delete or edit post created
        by another user  - page will be re-rendered with an
        error message.
        If edited post has no subject or content - page
        will be re-rendered with error message.
        :param post_id:
        :return:
        """
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
            # here - sometimes  database does not get updated before redirect
            # when application is run locally
            post.put()
            time.sleep(50/1000.0)

            self.redirect('/recentposts/%s' % str(post.key().id()))
        else:
            error = "Error: need both content and subject"
            self.render("edit_post.html", error=error)
