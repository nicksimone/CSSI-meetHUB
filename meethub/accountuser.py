from google.appengine.ext import ndb

class CssiUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()

class Activity(ndb.Model):
    # title = ndb.StringProperty()
    name = ndb.StringProperty()
