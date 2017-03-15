#!/usr/bin/env python
import os
import jinja2
import webapp2
import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        hidden_number = random.randint(1, 100)
        guessed_number = int(self.request.get("number"))
        if guessed_number == hidden_number:
            guessed_dict = {"guessed_number": guessed_number}
            return self.render_template("index.html", guessed_dict)
        else:
            hidden_dict = {"hidden_number": hidden_number}
            return self.render_template("index.html", hidden_dict)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
