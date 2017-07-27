from google.appengine.ext import ndb

class CssiUser(ndb.Model):
    userID = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

class Activity(ndb.Model):
    # title = ndb.StringProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    # user_key = ndb.KeyProperty(CssiUser)
    author = ndb.StringProperty()
