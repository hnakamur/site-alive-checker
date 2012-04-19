#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import webapp2
from webapp2_extras import jinja2

class WSGIApplication(webapp2.WSGIApplication):
  def __init__(self, *args, **kwargs):
    super(WSGIApplication, self).__init__(*args, **kwargs)
    self.router.set_dispatcher(self.__class__.custom_dispatcher)

  @staticmethod
  def custom_dispatcher(router, request, response):
    rv = router.default_dispatcher(request, response)
    if isinstance(rv, basestring):
      rv = webapp2.Response(rv)
    elif isinstance(rv, tuple):
      rv = webapp2.Response(*rv)
    elif isinstance(rv, dict):
      rv = webapp2.Response(**rv)

    return rv

  def route(self, *args, **kwargs):
    def wrapper(func):
      self.router.add(webapp2.Route(handler=func, *args, **kwargs))
      return func

    return wrapper

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render(self, filename, **template_args):
    return self.jinja2.render_template(filename, **template_args)
