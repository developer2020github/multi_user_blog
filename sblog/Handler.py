#this module contains definition of a basic handler class 
#from which other handlers in the application will be inheriting 

import webapp2
import jinja2
import os
import re
import HashLib


class Handler(webapp2.RequestHandler):

    def __init__(self, *a, **kw): 
        super(Handler, self).__init__(*a, **kw)
        self.template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env =jinja2.Environment(loader = jinja2.FileSystemLoader(self.template_dir), autoescape = True)
        self.user_name_regex_pattern = re.compile(r"^[a-zA-Z0-9_]*$")
        # ref. http: // www.regular - expressions.info / email.html
        self.email_address_regex_pattern = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = self.jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def email_string_ok(self, email, error_message_name, template_name):
        if not self.email_address_regex_pattern.match(email):
            self.render(template_name, **{error_message_name: "Error: email not valid"})
            return False
        return True

    def user_name_string_ok(self, string_to_check, error_message_name,
                              name_of_checked_variable, template_name):

        if string_to_check == "":
            self.render(template_name, **{error_message_name: "Error: " + name_of_checked_variable + " cannot be empty"})
            return False

        if not self.user_name_regex_pattern.match(string_to_check):
            self.render(template_name, **{error_message_name: "Error: " + name_of_checked_variable +
                                                              " can contain  only alphanumeric characters and _"})
            return False

        return True

    def get_logged_in_name(self):
        user_name = HashLib.get_secure_cookie_value(self, "user_id")
        return user_name
