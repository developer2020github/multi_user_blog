#this module contains definition of a basic handler class 
#from which other handlers in the application will be inheriting 

import webapp2
import jinja2
import os
import HashLib

class Handler(webapp2.RequestHandler):

    not_allowed_characters = ["|", ","]

    def __init__(self, *a, **kw): 
        super(Handler, self).__init__(*a, **kw)
        self.template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env =jinja2.Environment(loader = jinja2.FileSystemLoader(self.template_dir), autoescape = True)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = self.jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get_not_allowed_character(self, s):

        not_allowed_characters = ""

        for ch in self.not_allowed_characters:
            if ch in s:
                not_allowed_characters += ch + " "
        return not_allowed_characters

    def string_is_empty_or_contains_not_allowed_characters(self, string_to_check, error_message_name,
                                                           name_of_checked_variable, template_name):
        if string_to_check == "":
            self.render(template_name, **{error_message_name: "Error: " + name_of_checked_variable + " cannot be empty"})
            return True

        not_allowed_characters = self.get_not_allowed_character(string_to_check)
        if not_allowed_characters != "":
            self.render(template_name, **{error_message_name: "Error: " + name_of_checked_variable +
                                                              " cannot contain " + not_allowed_characters})
            return True

        return False

    def get_logged_in_name(self, default_name = "Guest"):
        user_name = HashLib.get_secure_cookie_value(self, "user_id")
        logged_in_name = default_name
        if user_name is not None:
            logged_in_name = user_name
        return logged_in_name