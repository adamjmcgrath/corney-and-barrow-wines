#!/usr/bin/env python2.5

from google.appengine.api import urlfetch
from google.appengine.ext import deferred
from google.appengine.ext import webapp

import base64
import logging
import models
import os
import readexcel


def handle_xl(row):
  key_name = base64.b64encode(row['click here'].encode('utf-8'))
  if key_name and not (models.Wine.get_by_key_name(key_name)):
    price_per = str(row['Price Per']).strip().upper()
    total_price = float(row['Price (duty paid inc VAT)'])
    price_per_bottle = total_price
    if price_per.startswith('CASE'):
      price_per_bottle = total_price / float(row['Unit Per Case'])

    w = models.Wine(key_name=key_name,
                    bottles=row['Bottles'],
                    cases=row['Cases'],
                    country_region=row['Country/Region'],
                    description=row['Description'],
                    label_condition=row['Label Condition'],
                    packaging=row['Packaging'],
                    price_duty_paid_ex_vat=str(row['Price (duty paid ex VAT)']),
                    price_duty_paid_inc_vat=str(row['Price (duty paid inc VAT)']),
                    price_in_bond=str(row['Price (in bond)']),
                    price_per=price_per,
                    price_per_bottle=price_per_bottle,
                    status=row['Status'],
                    ullage=row['Ullage'],
                    unit_per_case=row['Unit Per Case'],
                    unit_size=row['Unit Size'],
                    link=row['click here'],
                    vintage=row['Vintage'],
                    is_new=True,)
    w.put()
    logging.info('New wine added: %s' % row['Description'])


class GetWines(webapp.RequestHandler):
  def get(self):
    url = 'http://www.corneyandbarrow.com/images/assets/document/CustomerReport.xls'
    result = urlfetch.fetch(url)
    xl = readexcel.readexcel(file_contents=result.content)
    sheetnames = xl.worksheets()
    new_wines = []
    for sheet in sheetnames:
      for row in xl.getiter(sheet):
        deferred.defer(handle_xl, row)
