import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)
    
  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

class MainPage(Handler):
  def get(self):
    self.response.write('<h1>Main page</h1>')

class Rot13Handler(Handler):
  def get(self):
    self.render('rot13.html', text_output='')

  def post(self):
    text_input = self.request.get("text")
    text_output = ''
    for letter in text_input:
      if letter.isalpha():
        if not chr(ord(letter) + 13).isalpha():
          text_output += chr(ord(letter) - 13) 
        else: 
          text_output += chr(ord(letter) + 13)
      else:
        text_output += letter

    print text_output
    self.render('rot13.html', text_output = text_output)

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/rot13', Rot13Handler)
])