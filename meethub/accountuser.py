from google.appengine.ext import ndb

class Account(ndb.Model()):
    account_username = ndb.StringProperty()
    account_password = ndb.StringProperty()
