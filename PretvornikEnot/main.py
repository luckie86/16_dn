#!/usr/bin/env python
import os
import jinja2
import webapp2


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
        number = float(self.request.get("number"))
        operation = self.request.get("operation")

        km_miles = None
        miles_km = None
        if operation == "km/miles":
            km_miles = number * 0.621371192
        elif operation == "miles/km":
            miles_km = number * 1.609344

        result_dict = {
            "km_miles": km_miles,
            "miles_km": miles_km,
            "number": number,
        }

        return self.render_template("index.html", result_dict)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
