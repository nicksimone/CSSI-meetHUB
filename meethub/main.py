
import webapp2
import jinja2
import user

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env2 = jinja2.Environment(loader=jinja2.FileSystemLoader('static_files'))

from google.appengine.api import users
from accountuser import Post
from accountuser import CssiUser


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user is logged in...
        if user:
            email_address = user.nickname()
            # We could also do a standard query, but ID is special and it
            # has a special method to retrieve entries using it.
            cssi_user = CssiUser.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            # If the user has previously been to our site, we greet them!
            if cssi_user:
                self.response.write('''
                    Welcome %s %s (%s)! <br> %s <br>''' % (
                        cssi_user.first_name,
                        cssi_user.last_name,
                        email_address,
                        signout_link_html))
            # If the user hasn't been to our site, we ask them to sign up
            else:
                self.response.write('''
                    Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action="/">
                    <input type="text" name="first_name">
                    <input type="text" name="last_name">
                    <input type="submit">
                    </form><br> %s <br>
                    ''' % (email_address, signout_link_html))
        # Otherwise, the user isn't logged in!
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (
                    users.create_login_url('/')))

    def post(self):
        user = users.get_current_user()
        if not user:
            # You shouldn't be able to get here without being logged in
            self.error(500)
            return
        cssi_user = CssiUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            # ID Is a special field that all ndb Models have, and esnures
            # uniquenes (only one user in the datastore can have this ID.
            id=user.user_id())
        cssi_user.put()
        self.response.write('Thanks for signing up, %s!' %
            cssi_user.first_name)


#class SignInHandler(webapp2.RequestHandler):
    #def get(self):
        #main_template = env.get_template('index.html')
        #self.response.write(main_template.render())
        #self.request.get('account_username')
        #self.request.get('account_password')
# class SignUpHandler(webapp2.RequestHandler):
#     def get(self):

#class CreatePost(webapp2.RequestHandler):
    #def Post(self):
        #new_post = Post(content= self.request.get('post')
        #posts_template = env.get_template('posts.html')
        #self.response.write(posts_template.render(Posts))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
    # ('/signin', SignInHandler),
    #('/', SignUpHandler),
], debug=True)
