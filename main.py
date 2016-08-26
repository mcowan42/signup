import webapp2
import cgi
import re
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):


    def get(self):
        t = jinja_env.get_template("signup-form.html")
        response = t.render(username="",password="",verify="",email="",error_username="",error_password="",error_verify="",error_email="")
        self.response.write(response)

    def post(self):
        errorflag = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        error_username=""
        error_password=""
        error_verify=""
        error_email=""

        if not valid_username(username):
            errorflag=True
            error_username = "That's not a valid username."

        if not valid_password(password):
            errorflag=True
            error_password = "That wasn't a valid password."
        elif (password != verify):
            errorflag=True
            error_verify = "Your passwords didn't match."

        if not valid_email(email):
            errorflag=True
            error_email = "That's not a valid email."

        password=""
        verify=""

        if errorflag:
            t = jinja_env.get_template("signup-form.html")
            response = t.render(username=username,password="",verify="",email=email,
                error_username=error_username,error_password=error_password,error_verify=error_verify,error_email=error_email)
            self.response.write(response)
        else:
            self.redirect('/welcome/?username='+ username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username=self.request.get('username')

        page_header="""
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>Welcome</title>
                    </head>

                    <body>
                """

        page_footer="""
                    </body>
                    </html>
                """

        welcome_message="Welcome " + username
        response=page_header + welcome_message + page_footer
        self.response.write(response)

    def post(self):
        username = self.request.get('username')
        if not valid_username(username):
            self.redirect('/')



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome/', Welcome)
], debug=True)
