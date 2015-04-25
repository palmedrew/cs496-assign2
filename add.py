import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs

class Add(base_page.BaseHandler):
  def __init__(self, request, response):
    self.initialize(request, response)
    self.template_values = {}
    if self.request.get('message'):
      self.template_values['message'] = self.request.get('message')
    
  def render(self, page):
    self.template_values['checks'] = [{'name':x.name, 'key':x.key.urlsafe()} 
    for x in db_defs.CheckBox.query(ancestor=ndb.Key(db_defs.CheckBox, self.app.config.get('default-group'))).fetch()]
    
    self.template_values['radios'] = [{'name':x.name, 'key':x.key.urlsafe()} 
    for x in db_defs.RadioButton.query(ancestor=ndb.Key(db_defs.RadioButton, self.app.config.get('default-group'))).fetch()]
    
    self.template_values['items'] = [{'name':x.name, 'key':x.key.urlsafe()} 
    for x in db_defs.MainItem.query(ancestor=ndb.Key(db_defs.MainItem, self.app.config.get('default-group'))).fetch()]
    
    base_page.BaseHandler.render(self, page, self.template_values)
    
  def get(self):
    self.render('add.html')
    
  def post(self):
    action = self.request.get('action')
    if action == 'add_main':
      item_name = self.request.get('main-name')
      if item_name not in [ ti.name for ti in db_defs.MainItem.query().fetch()]:
      #construct Key(Kind, value)
        k = ndb.Key(db_defs.MainItem, self.app.config.get('default-group'))
      #call constructor
        mi = db_defs.MainItem(parent=k)
      #populate
        mi.name = item_name
        mi.chkboxes = [ndb.Key(urlsafe=x) for x in self.request.get_all('checks[]')]
        if self.request.get('rdiobtn'):
          mi.rdiobtn = ndb.Key(urlsafe=self.request.get('rdiobtn'))
        else:
          mi.rdiobtn = None
        mi.email = self.request.get('email')
        mi.phone = self.request.get('phone')
      #add to ndb
        mi_key = mi.put()
        self.redirect('/edit?key=' + mi_key.urlsafe() + '&dbkind=MainItem&action=view')
      else:
        self.template_values['message'] = 'ERROR: ' + item_name + ' already exists!'
        self.render('add.html')
    elif action == 'add_checkbox':
      check_name = self.request.get('checkbox-name')
      if check_name not in [ tc.name for tc in db_defs.CheckBox.query().fetch() ]:
        k = ndb.Key(db_defs.CheckBox, self.app.config.get('default-group'))
        c = db_defs.CheckBox(parent=k)
        c.name = check_name
        c_key = c.put()
        self.redirect('/edit?key=' + c_key.urlsafe() + '&dbkind=CheckBox&action=view')
      else:
        self.template_values['message'] = 'ERROR: ' + check_name + ' already exists!'
        self.render('add.html')
    elif action == 'add_radiobutton':
      radio_name = self.request.get('radiobutton-name')
      if radio_name not in [ tr.name for tr in db_defs.RadioButton.query().fetch() ]:
        k = ndb.Key(db_defs.RadioButton, self.app.config.get('default-group'))
        r = db_defs.RadioButton(parent=k)
        r.name = radio_name
        r_key = r.put()
        self.redirect('/edit?key=' + r_key.urlsafe() + '&dbkind=RadioButton&action=view')
      else:
        self.template_values['message'] = 'ERROR: ' + radio_name + ' already exists!'
        self.render('add.html')
    else:
      self.template_values['message'] = 'Action ' + action + ' is unknown.'
      self.render('add.html')