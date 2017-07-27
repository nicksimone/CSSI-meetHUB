
import webapp2
import jinja2
import logging
import user
from datetime import datetime
import time

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env2 = jinja2.Environment(loader=jinja2.FileSystemLoader('static_files'))

from google.appengine.api import users
from accountuser import Activity
from accountuser import CssiUser


# global cssi_user_key



class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        # If the user is logged in...
        if user:
            email_address = user.nickname()
            # We could also do a standard query, but ID is special and it
            # has a special method to retrieve entries using it.
            cssi_user = CssiUser.get_by_id(user.user_id())
            signout_link_html = '  <link rel="stylesheet" href="static/mainhub.css"></link> <a href="%s">Enter the HUB</a>' % (
                users.create_logout_url('/createpost'))
            # If the user has previously been to our site, we greet them!
            if cssi_user:
                self.response.write('''
                      <link rel="stylesheet" href="static/mainhub.css"></link>Welcome %s %s (%s)! <br> %s <br>''' % (
                        cssi_user.first_name,
                        cssi_user.last_name,
                        email_address,
                        signout_link_html))
            # If the user hasn't been to our site, we ask them to sign up
            else:
                self.response.write('''  <link rel="stylesheet" href="static/mainhub.css"></link>
                    Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action="/">
                    First Name: <input type="text" name="first_name"> <br>
                    Last Name: <input type="text" name="last_name"> <br>
                    Username: <input type="text" name="userID"> <br>
                    <input type="submit">
                    </form>
                    ''' % (email_address))
        # Otherwise, the user isn't logged in!
        else:
            self.response.write('''  <link rel="stylesheet" href="static/mainhub.css"></link>
                <h1 class= "login">Welcome to meetHUB!</h1> <br>
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
            #userID=self.request.get('userID')
            # ID Is a special field that all ndb Models have, and esnures
            # uniquenes (only one user in the datastore can have this ID.
            id=user.user_id())


        # global cssi_user_key
        # cssi_user_key = cssi_user.put()



        signout_link_html = '<a href="%s">Enter the HUB</a>' % (
            users.create_logout_url('/createpost'))
        # cssi_user.put()
        self.response.write('  <link rel="stylesheet" href="static/mainhub.css"></link>Thanks for signing up, %s! <br> %s' % (
            cssi_user.first_name,
            signout_link_html))

class DeleteDatabase(webapp2.RequestHandler):
    def get(self):
        query = CssiUser.query()
        all_users = query.fetch()
        for person in all_users:
          person.key.delete()
        query2 = Activity.query()
        all_activities = query2.fetch()
        for act in all_activities:
          act.key.delete()

class CreatePost(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        # user_key = user.get('key')
        # console.log(user_key)
        # theId = user.user_id()

        main_template = env.get_template('mainhub.html')
        blog_posts = Activity.query().order(-Activity.date).fetch()
        variables = {'posts': blog_posts}
        self.response.write(main_template.render(variables))
    def post(self):
        post_date = datetime.now()
        # text_input = self.request.get('activity_name')



        # global cssi_user_key

        new_post = Activity(name = self.request.get('activity_name'), date = post_date, author=self.request.get('activity_author'))
        new_post.put()
        # console.log(new_post)
        time.sleep(1)
        blog_posts = Activity.query().order(-Activity.date).fetch()
        variables = {'posts':blog_posts}
        posts_template = env.get_template('mainhub.html')
        self.response.write(posts_template.render(variables))


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('search.html')
        self.response.write(main_template.render())
    def post(self):
        username = self.request.get('search_name')
        all_users = CssiUser.query().fetch()
        variables = {'usernames': all_users}
        search_template = env.get_template('search.html')
        self.response.write(search_template.render(variables))
        # for u_name in all_users:
        #     if username == u_name.userID:
        #         logging.info(u_name.userID)
        # json_string = self.request.body
        # json_object = json.loads(json_string)
        # items = json_object['items']
        # friend_user_name = (json_object['name'])
        # reply_data = {
        # 'name': friend_user_name
        # }
        # self.response.headers['Content-Type'] = "application/json"
        # self.response.write(json.dumps(reply_data))



#cssi_user = CssiUser(userID="ndsimone", first_name = "Nick", last_name = "dane")
#cssi_user_key = cssi_user.put()
#         all_users = CssiUser.query().fetch()
# username = "ndsimone"
# for u_name in all_users:
#   if username == u_name.userID:
#     print "Yes"

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/createpost', CreatePost),
    ('/deletedatabase', DeleteDatabase),
    ('/search', SearchHandler)
], debug=True)
