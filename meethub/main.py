
import webapp2
import jinja2
import user

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env2 = jinja2.Environment(loader=jinja2.FileSystemLoader('static_files'))

from google.appengine.api import users
from accountuser import Activity
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
            signout_link_html = '<a href="%s">Enter the HUB</a>' % (
                users.create_logout_url('/createpost'))
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
                Welcome to meetHUB! <br>
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
        signout_link_html = '<a href="%s">Enter the HUB</a>' % (
            users.create_logout_url('/createpost'))
        cssi_user.put()
        self.response.write('Thanks for signing up, %s! <br> %s' % (
            cssi_user.first_name,
            signout_link_html))





class CreatePost(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('mainhub.html')
        self.response.write(main_template.render())
    def post(self):
        # text_input = self.request.get('activity_name')
        new_post = Activity(name = self.request.get('activity_name'))
        new_post.put()
        posts_template = env.get_template('mainhub.html')
        self.response.write(posts_template.render(Activity))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/createpost', CreatePost),
    #('/', SignUpHandler),
], debug=True)
