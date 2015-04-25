import webapp2

config = {'default-group':'base-data'}

application = webapp2.WSGIApplication([
  ('/add', 'add.Add'),
  ('/edit', 'edit.Edit'),
  ('/', 'add.Add'),
], debug=True, config=config)