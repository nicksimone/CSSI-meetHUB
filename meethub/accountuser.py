from google.appengine.ext import ndb

class CssiUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

class Post(ndb.Model):
    # title = ndb.StringProperty()
    content = ndb.StringProperty()
