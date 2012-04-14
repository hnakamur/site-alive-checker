from datetime import datetime
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Hello, webapp World!')

class SendMail(webapp.RequestHandler):
  def get(self):
    sendMail()
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Sent mail.')

def sendMail(body="Site is not alive"):
  mail.send_mail(
     sender="site alive cheker <hnakamur@gmail.com>",
     to="hnakamur+sitealivechecker@gmail.com",
     subject="site is not alive",
     body=body)

class CheckSiteForever(webapp.RequestHandler):
  def get(self):
    try:
      result = urlfetch.fetch(url="http://naruh.net/")
      if result.status_code != 200:
        sendMail("%s Status code=%d" % (datetime.now(), result.status_code))
      self.response.out.write("Status=%d" % result.status_code)
    except urlfetch.DownloadError, e:
      sendMail("Error: %s" % e)
    taskqueue.add(url='/checksiteforever', method='GET', countdown=30)

class CheckSite(webapp.RequestHandler):
  def get(self):
    try:
      result = urlfetch.fetch(url="http://naruh.net/")
      if result.status_code != 200:
        sendMail("Status code=%d" % result.status_code)
      self.response.out.write("Status=%d" % result.status_code)
    except urlfetch.DownloadError, e:
      sendMail("Error: %s" % e)

application = webapp.WSGIApplication(
    [
      ('/', MainPage),
      ('/checksite', CheckSite),
      ('/checksiteforever', CheckSiteForever),
      ('/sendmail', SendMail),
    ],
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
