#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
from webapp2 import redirect
import micro_webapp2
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
from google.appengine.ext import db
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


app = micro_webapp2.WSGIApplication()

@app.route('/')
@app.route('/sites')
def sites(request):
  sites = Site.gql('ORDER BY created_at DESC').fetch(LIST_LIMIT)
  return app.render('index.html', sites=sites)

@app.route('/sites/add', methods='GET')
def showAddSiteForm(request):
  form = SiteForm()
  return app.render('add_site.html', form=form)

@app.route('/sites/add', methods='POST')
def addSite(request):
  form = SiteForm(request.POST)
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
    return app.render('add_site.html', form=form)

@app.route('/site/<key>', methods='GET')
def showSiteForm(request, key):
  site = db.get(key)
  form = SiteForm(name=site.name,
                  url=site.url,
                  sender=site.sender,
                  recipient=site.recipient,
                  subject=site.subject,
                  interval_minutes=site.interval_minutes,
                  watching_enabled=site.watching_enabled)
  return app.render('edit_site.html', key=key, form=form)

@app.route('/site/<key>', methods='POST')
def updateSite(request, key):
  form = SiteForm(request.POST)
  if form.validate():
    action = request.POST['action']
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
    return app.render('add_site.html', form=form)

def enqueueCheck(site):
  taskqueue.add(url='/site/%s/loopcheck' % site.key(), method='POST',
      countdown=site.interval_minutes*60)

@app.route('/site/<key>/loopcheck', methods='POST')
def loopCheck(request, key):
  site = db.get(key)
  if site and site.watching_enabled:
    try:
      result = urlfetch.fetch(url=site.url)
      if result.status_code != 200:
        sendMail(site, "%s Status code=%d" % (datetime.now(), result.status_code))
    except urlfetch.DownloadError, e:
      sendMail(site, "Error: %s" % e)
    enqueueCheck(site)

def sendMail(site, body="Site is not alive"):
  mail.send_mail(
     sender=site.sender,
     to=site.recipient,
     subject=site.subject,
     body=body)
