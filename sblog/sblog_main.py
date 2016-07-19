#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#http://sblog-1372.appspot.com/

'''
main page: * front end prototype complere
shows sign in form -> if user name and password are correct, takes user to welcome  page with link to other pages
                            (can have some sort of  user activity record)
                         if use name and password are incpre incorrect - takes user to signup page
         signup link -> takes to signup page
         read recent posts link -> takes to recent posts page

welcome page; * front end protorype complete
        shows message "Welcome!" + user name
        has links to: recent posts
                      new post
                      log out

signup page: *front end protytype complete
        has signup form
        redirects to welcome page
        has link to sign in page (in case user got here by mistake)

signin page: * front end protype complete
        has sign in form
        redirects to welcome page

recent posts page: * front end protype complete
      shows 10 most recent posts
      has links to:
                    new post
                    sign in
                    sign up
                    log out
new post page: * front end protype complete
     if user is signed in: allows to add new post . redirects to current post poage
     if user is not signed up: redirects to signup page

current post page: *front end prototype complete
    shows current post.
    has links to recent posts page and logout

logout page: * front end prototype complete
takes to main page

'''
import webapp2
import jinja2
from Handler import Handler
from RecentPostsHandler import RecentPostsHandler
from SignUpHandler import SignUpHandler
from WelcomeHandler import WelcomeHandler
from NewPostHandler import NewPostHandler
from LogOutHandler import LogOutHandler
from LogInHandler import LogInHandler
from CurrentPostHandler import CurrentPostHandler

class MainPageHandler(Handler):

    def get(self):
        self.render("main.html")

    def post(self):
        username=self.request.get("username")
        password = self.request.get("password")
        #check user name and password here
        self.redirect("/welcome")


app = webapp2.WSGIApplication([
    ('/', MainPageHandler), 
    ('/recentposts', RecentPostsHandler),
    ('/signeup', SignUpHandler),
    ("/welcome", WelcomeHandler),
    ("/newpost", NewPostHandler),
    ("/login", LogInHandler),
    ("/logout", LogOutHandler),
    ('/recentposts/([0-9]+)', CurrentPostHandler)
], debug=True)
