#this module contains definition of a basic handler class 
#from which other handlers in the application will be inheriting 

import webapp2
import jinja2
import os


class Handler(webapp2.RequestHandler):

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