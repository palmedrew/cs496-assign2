import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs

class Edit(base_page.BaseHandler):
  def __init__(self, request, response):
    self.initialize(request, response)
    self.template_values = {}
    if self.request.get('message'):
      self.template_values['message'] = self.request.get('message')
      
  def get(self):
    dbkind = self.request.get('dbkind')
    self.template_values['dbkind'] = dbkind
    if self.request.get('action') == "edit":
      self.template_values['action_page'] = "/edit"
    thing_key = ndb.Key(urlsafe=self.request.get('key'))
    thing = thing_key.get()
    self.template_values['thing'] = thing
    
    if dbkind == 'MainItem':
      checkboxes = db_defs.CheckBox.query(ancestor=ndb.Key(db_defs.CheckBox, 
      self.app.config.get('default-group'))).fetch()
      check_boxes = []
      for c in checkboxes:
        if c.key in thing.chkboxes:
          check_boxes.append({'name':c.name, 'key':c.key.urlsafe(), 'checked':True})
        else:
          check_boxes.append({'name':c.name, 'key':c.key.urlsafe(), 'checked':False})
      self.template_values['checks'] = check_boxes
      radiobuttons = db_defs.RadioButton.query(ancestor=ndb.Key(db_defs.RadioButton, 
      self.app.config.get('default-group'))).fetch()
      radio_buttons = []
      for r in radiobuttons:
        if r.key == thing.rdiobtn:
          radio_buttons.append({'name':r.name, 'key':r.key.urlsafe(), 'checked':True})
        else:
          radio_buttons.append({'name':r.name, 'key':r.key.urlsafe(), 'checked':False})
      self.template_values['radios'] = radio_buttons
    
    self.render('edit.html', self.template_values)
    
  def post(self):
    delete_key = False
    name_exists = False
    something_changed = False
    dbkind = self.request.get('dbkind')
    self.template_values['dbkind'] = dbkind
    
    self.template_values['action_page'] = "/edit"
    if self.request.get('action') == "delete":
      delete_key = True
    thing_key = ndb.Key(urlsafe=self.request.get('key'))
    thing = thing_key.get()
    self.template_values['thing'] = thing
    thing_name = self.request.get('item-name')
    if thing_name != thing.name:
      name_change = True
    
    
    if dbkind in ["MainItem", "RadioButton", "CheckBox"]:
      if thing_name != thing.name:
        if dbkind == "RadioButton":
          if thing_name not in [ tt.name for tt in db_defs.RadioButton.query().fetch()]:
            thing.name = thing_name
            something_changed = True
          else:
            name_exists = True
      
        elif dbkind == "CheckBox":
          if thing_name not in [ tt.name for tt in db_defs.CheckBox.query().fetch()]:
            thing.name = thing_name
            something_changed = True
          else:
            name_exists = True
      
        elif dbkind == "MainItem":
          if thing_name not in [ tt.name for tt in db_defs.MainItem.query().fetch()]:
            thing.name = thing_name
            something_changed = True
          else:
            self.template_values['message'] = 'ERROR: ' + thing_name + ' exists!'
            name_exists = True
      
      if dbkind == "MainItem":
        if not delete_key:
          thing_email = self.request.get('email')
          thing_phone = self.request.get('phone')
          word = self.request.get('rdiobtn')
          if word == None or not word:
            thing_rdiobtn=None
          else:            
            thing_rdiobtn = ndb.Key(urlsafe=word)
          thing_checks = [ndb.Key(urlsafe=x) for x in self.request.get_all('checks[]')]
         
          if thing_email != thing.email:
            thing.email = thing_email
            something_changed = True
          if thing_phone != thing.phone:
            thing.phone = thing_phone
            something_changed = True
          if thing_rdiobtn != thing.rdiobtn:
            thing.rdiobtn = thing_rdiobtn
            something_changed = True
           
          for tc in thing_checks:
            if tc not in thing.chkboxes:
              thing.chkboxes = thing_checks
              something_changed = True
              break
      
      if dbkind == "MainItem" and delete_key:
        #self.template_values['message'] += 'Deleted ' + dbkind
        thing_key.delete()
        #self.render('add.html', self.template_values)
        self.redirect('/add?message="Deleted ' + dbkind + '"')    
      elif name_exists:
        #self.template_values['message'] += 'Name: ' + thing_name + ' already exists!'
        self.redirect('/edit?key=' + thing_key.urlsafe() + '&dbkind=' + dbkind + '&action=edit'
        + '&message="Name: ' + thing_name + ' exists"')
        #self.render('edit.html', self.template_values)
      elif something_changed and not name_exists and not delete_key:
        thing.put()
        #self.template_values['message'] += thing.name + ' has been edited.'
        self.redirect('/edit?key=' + thing_key.urlsafe() + '&dbkind=' + dbkind + '&action=view'
        + '&message="' + thing.name + ' has been edited"')
      elif not something_changed:
        #self.template_values['message'] += 'Nothing Has Been Changed.'
        #self.render('edit.html', self.template_values)
        self.redirect('/edit?key=' + thing_key.urlsafe() + '&dbkind=' + dbkind + '&action=edit'
        + '&message="Nothing changed"')
      else:
        self.template_values['message'] = 'Unknow set of actions and/or variables'
        self.render('add.html', self.template_values)
        #self.redirect('/add?message="Unknow set of actions and/or variables"') 
        
      
        
    else:
      self.template_values['message'] = 'Unknow ndb kind: ' + dbkind
      self.render('add.html', self.template_values)
      #self.redirect('/add?message="Unknown ndb kind: ' + dbkind + '"')
