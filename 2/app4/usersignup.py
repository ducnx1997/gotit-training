import os
import webapp2
import jinja2
import re

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

def valid_username(username):
  return re.compile("^[a-zA-Z0-9_-]{3,20}$").match(username)

def valid_password(password):
  return re.compile("^.{3,20}$").match(password)

def valid_email(email):
  return re.compile("^[\S]+@[\S]+.[\S]+$").match(email)

class SignupHandler(Handler):
  def get(self):
    self.render('signup.html', 
      invalid_username_msg='',
      invalid_password_msg='',
      invalid_2ndpassword_msg='',
      invalid_email_msg='',
      password = '',
      username = '',
      verify = '',
      email = '')

  def post(self):
    username = self.request.get("username")
    password = self.request.get("password")
    verify_password = self.request.get("verify")
    email = self.request.get("email")
    if valid_username(username): 
      invalid_username_msg=''
    else:
      invalid_username_msg='That\'s not a valid username.'
    if valid_password(password):
      invalid_password_msg=''
    else:
      invalid_password_msg='That wasn\'t a valid password.'
    if password and password != verify_password:
      invalid_2ndpassword_msg='Your passwords didn\'t match'
    else:
      invalid_2ndpassword_msg=''
    if valid_email(email):
      invalid_email_msg=''
    else:
      invalid_email_msg='That\'s not a valid email.'
    self.render('signup.html',
      invalid_username_msg = invalid_username_msg,
      invalid_password_msg = invalid_password_msg,
      invalid_2ndpassword_msg = invalid_2ndpassword_msg,
      invalid_email_msg = invalid_email_msg,
      username = username,
      password = password,
      verify = verify_password,
      email = email
      )
      
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/signup', SignupHandler)
], debug=True)