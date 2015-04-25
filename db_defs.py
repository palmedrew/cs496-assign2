from google.appengine.ext import ndb
  
class MainItem(ndb.Model):
  name = ndb.StringProperty(required=True)
  chkboxes = ndb.KeyProperty(kind="CheckBox", repeated=True)
  rdiobtn = ndb.KeyProperty(kind="RadioButton")
  phone = ndb.StringProperty()
  email = ndb.StringProperty()

class CheckBox(ndb.Model):
  name = ndb.StringProperty(required=True)
  
class RadioButton(ndb.Model):
  name = ndb.StringProperty(required=True)
