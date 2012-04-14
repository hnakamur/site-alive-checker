from bottle import default_app, get, jinja2_template as template
from google.appengine.ext.webapp.util import run_wsgi_app

@get('/hello')
@get('/hello/')
@get('/hello/:name')
@get('/goodbye/:name')
def index(name='World'):
  return '<b>Hello %s!</b>' % name

@get('/titles')
def titles():
  return template('templates/home', titles=['hi', 'lo'])

def main():
  run_wsgi_app(default_app())

if __name__ == '__main__':
  main()
