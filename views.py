#!/usr/bin/env python2.5

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import mail

import logging
import models
import os


class ShowWines(webapp.RequestHandler):
  def get(self):
    orderby = self.request.get('orderby')
    direction = self.request.get('direction')
    cursor = self.request.get('cursor')
    if (orderby and orderby in ['price_per_bottle', 'vintage', 'date'] and direction and direction in ['asc', 'desc']):
      gql = 'ORDER BY %s %s, %s' % (orderby, direction.upper(), 'price_per_bottle' if orderby == 'vintage' else 'vintage')
    else:
      gql = 'ORDER BY date DESC, vintage'

    q = models.Wine.gql(gql)

    if cursor:
      q.with_cursor(start_cursor=cursor)

    template_values = {
      'wines': q.fetch(20),
      'cursor': q.cursor(),
      'orderby': orderby,
      'direction': direction,
    }
    path = os.path.join(os.path.dirname(__file__), 'home.html')
    self.response.out.write(template.render(path, template_values))


class Wine(webapp.RequestHandler):
  def get(self, key):
    template_values = {
      'wine': models.Wine.get(key),
    }
    path = os.path.join(os.path.dirname(__file__), 'wine.html')
    self.response.out.write(template.render(path, template_values))


class SendEmail(webapp.RequestHandler):
  def get(self):
    wines = models.Wine.gql('WHERE is_new = True ORDER BY date DESC, vintage').fetch(500)
    wine_arr = []
    for wine in wines:
      wine.is_new = False
      wine.put()
      wine_arr.append(wine)
    if len(wine_arr):
      template_values = {
        'wines': wine_arr,
        'is_email': True
      }
      path = os.path.join(os.path.dirname(__file__), 'wines.html')
      mail.send_mail(sender="adamjmcgrath@gmail.com",
                     to="adamjmcgrath@gmail.com, Thomas.Holmes@miller-insurance.com, SHolmes@imgworld.com",
                     subject="New wines on Corney & Barrow",
                     body="View in HTML",
                     html=template.render(path, template_values))
      logging.info('email sent')
