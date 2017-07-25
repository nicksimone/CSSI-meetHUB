
import webapp2
import jinja2
import user

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env2 = jinja2.Environment(loader=jinja2.FileSystemLoader('static_files'))

from google.appengine.api import users
from accountuser import Post
import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/'))

        self.response.write('<html><body>%s</body></html>' % greeting)

        

class SignInHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('index.html')
        self.response.write(main_template.render())
        self.request.get('account_username')
        self.request.get('account_password')
# class SignUpHandler(webapp2.RequestHandler):
#     def get(self):

<<<<<<< HEAD

=======
class CreatePost(webapp2.RequestHandler):
    def Post(self):
        new_post = Post(content= self.request.get('post')
        posts_template = env.get_template('posts.html')
        self.response.write(posts_template.render(Posts))
>>>>>>> d9bbb6cefc7d146aab45049366b68116c94226ed

app = webapp2.WSGIApplication([
    ('/', MainPage),
    # ('/signin', SignInHandler),
    #('/', SignUpHandler),
], debug=True)
