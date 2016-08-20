"""This module contains definition of a base handler class
from which other handlers in the application inherit
"""

import os
import re
import webapp2
import jinja2


class Handler(webapp2.RequestHandler):
    """
    Base class for all other handlers in the application.
    Inherits from Reuqesthandler and adds application-specific
    functionality common to all other handlers.
    """

    def __init__(self, *a, **kw):
        """
        Sets templates directory,
        initializes Jinja2 environment and
        compiles reg expressions for user name and email validations
        """
        super(Handler, self).__init__(*a, **kw)
        self.template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_dir),
                                            autoescape=True)
        self.user_name_regex_pattern = re.compile(r"^[a-zA-Z0-9_]*$")
        # ref. http: // www.regular - expressions.info / email.html
        self.email_address_regex_pattern = \
            re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)

    def write(self, *a, **kw):
        """
        helper write function: writes a repsponse with provided arguments
        """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """
        Renders string from template.
        :param template:
        :param params: paramaters passed to Jinja2 template
        :return: rendered page
        """
        template_to_render = self.jinja_env.get_template(template)
        return template_to_render.render(params)

    def render(self, template, **kw):
        """
        Writes a response generated from template based
        on the list of arguments.
        :param template: template file
        :param kw: actual values for template parameters
        :return: None
        """
        self.write(self.render_str(template, **kw))

    def email_string_ok(self, email, error_message_name, template_name):
        """
        Validates e-mail vs e-mail regex and
        renders provided template with e-mail error message in
        case email is invalid
        :param email: email address sting
        :param error_message_name: template parameter name that displays error
        :param template_name: name of template file
        :return: True if email is valid, False otherwise
        """
        if not self.email_address_regex_pattern.match(email):
            self.render(template_name, **{error_message_name: "Error: email not valid"})
            return False
        return True

    def user_name_string_ok(self, string_to_check, error_message_name,
                            name_of_checked_variable, template_name):
        """
        Validates user name string  vs user name regex and
        renders provided template with a parameterized error message in
        case user name  is invalid
        :param string_to_check: user name string to be checked
        :param error_message_name: template parameter name that displays error
        :param name_of_checked_variable: variable name to be displayed inside
                                        the error message
        :param template_name: template file
        :return: True if user name is valid, False otherwise
        """
        if string_to_check == "":
            self.render(template_name, **{error_message_name: "Error: "
                                                              + name_of_checked_variable
                                                              + " cannot be empty"})
            return False

        if not self.user_name_regex_pattern.match(string_to_check):
            error_message = "Error: " + name_of_checked_variable \
                            + " can contain  only alphanumeric characters and _"
            self.render(template_name,
                        **{error_message_name: error_message})
            return False

        return True
