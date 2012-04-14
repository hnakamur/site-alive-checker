from bottle import default_app, get, post, redirect, jinja2_template as template
from google.appengine.ext.webapp.util import run_wsgi_app

@get('/')
@get('/sites')
def sites():
  sites = [
    {'name': 'naruh.net', 'url': 'http://naruh.net', 'recipient': 'hnakamur@gmail.com'},
    {'name': 'naruh.com', 'url': 'http://naruh.com', 'recipient': 'hnakamur@gmail.com'},
  ]
  return template('templates/index', sites=sites)

@get('/sites/add')
def showAddSiteForm():
  return template('templates/add_site')

@post('/sites/add')
def addSite():
  return redirect('/sites')

class StripPathMiddleware(object):
  def __init__(self, app):
    self.app = app
  def __call__(self, e, h):
    e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
    return self.app(e,h)

def main():
  run_wsgi_app(StripPathMiddleware(default_app()))

if __name__ == '__main__':
  main()
