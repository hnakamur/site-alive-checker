from bottle import (
  default_app, get, post, redirect, request, jinja2_template as template
)
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from wtforms import BooleanField, Form, SelectField, TextField
from wtforms.validators import Required, URL, Email

LIST_LIMIT = 10

class Site(db.Model):
  name = db.StringProperty(required=True)
  url = db.LinkProperty(required=True)
  interval_minutes = db.IntegerProperty(required=True)
  sender = db.EmailProperty(required=True)
  recipient = db.EmailProperty(required=True)
  subject = db.StringProperty(required=True)
  watching_enabled = db.BooleanProperty(required=True)
  created_at = db.DateTimeProperty(auto_now_add=True)
  updated_at = db.DateTimeProperty(auto_now=True)

class SiteForm(Form):
  name = TextField("Name", validators=[Required()])
  url = TextField("URL", validators=[Required(), URL()])
  interval_minutes = SelectField("Interval minutes",
    validators=[Required()],
    choices=[
      (1, '1 minute'),
      (2, '2 minutes'),
      (3, '3 minutes'),
      (4, '4 minutes'),
      (5, '5 minutes')
    ],
    coerce=int
  )
  sender = TextField("Sender email address",
    validators=[Required(), Email()]
  )
  recipient = TextField("Recipient email address",
    validators=[Required(), Email()]
  )
  subject = TextField("Mail subject", validators=[Required()])
  watching_enabled = BooleanField("Watching enabled")

@get('/')
@get('/sites')
def sites():
  sites = Site.gql('ORDER BY created_at DESC').fetch(LIST_LIMIT)
  return template('templates/index', sites=sites)

@get('/sites/add')
def showAddSiteForm():
  form = SiteForm()
  return template('templates/add_site', form=form)

@post('/sites/add')
def addSite():
  form = SiteForm(request.forms)
  if form.validate():
    site = Site(name=form['name'].data,
                 url=form['url'].data,
                 sender=form['sender'].data,
                 recipient=form['recipient'].data,
                 subject=form['subject'].data,
                 interval_minutes=form['interval_minutes'].data,
                 watching_enabled=form['watching_enabled'].data)
    site.put()
    if site.watching_enabled:
      enqueueCheck(site)
    return redirect('/sites')
  else:
    return template('templates/add_site', form=form)

@get('/site/:key')
def showSiteForm(key):
  site = db.get(key)
  form = SiteForm(name=site.name,
                  url=site.url,
                  sender=site.sender,
                  recipient=site.recipient,
                  subject=site.subject,
                  interval_minutes=site.interval_minutes,
                  watching_enabled=site.watching_enabled)
  return template('templates/edit_site', key=key, form=form)

@post('/site/:key')
def updateSite(key):
  form = SiteForm(request.forms)
  if form.validate():
    action = request.forms['action']
    if action == 'edit':
      site = db.get(key)
      site.name = form['name'].data
      site.url = form['url'].data
      site.sender = form['sender'].data
      site.recipient=form['recipient'].data
      site.subject = form['subject'].data
      site.interval_minutes=form['interval_minutes'].data
      if not site.watching_enabled and form['watching_enabled'].data:
        enqueueCheck(site)
      site.watching_enabled = form['watching_enabled'].data
      site.put()
    elif action == 'delete':
      db.delete(key)
    return redirect('/sites')
  else:
    return template('templates/add_site', form=form)

def enqueueCheck(site):
  taskqueue.add(url='/site/%s/loopcheck' % site.key(), method='POST',
      countdown=site.interval_minutes*60)

@post('/site/:key/loopcheck')
def loopCheck(key):
  site = db.get(key)
  if site and site.watching_enabled:
    try:
      result = urlfetch.fetch(url=site.url)
      if result.status_code != 200:
        sendMail(site, "%s Status code=%d" % (datetime.now(), result.status_code))
      self.response.out.write("Status=%d" % result.status_code)
    except urlfetch.DownloadError, e:
      sendMail(site, "Error: %s" % e)
    enqueueCheck(site)

def sendMail(site, body="Site is not alive"):
  mail.send_mail(
     sender=site.sender,
     to=site.recipient,
     subject=site.subject,
     body=body)

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
