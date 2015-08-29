#!/usr/bin/env python2.5

from google.appengine.ext import db

class Wine(db.Model):
  date = db.DateProperty(auto_now=True)
  country_region = db.StringProperty()
  vintage = db.StringProperty()
  description = db.StringProperty()
  unit_size = db.StringProperty()
  unit_per_case = db.StringProperty()
  bottles = db.StringProperty()
  cases = db.StringProperty()
  price_in_bond = db.StringProperty()
  price_duty_paid_ex_vat = db.StringProperty()
  price_duty_paid_inc_vat = db.StringProperty()
  price_per = db.StringProperty()
  status = db.StringProperty()
  ullage = db.StringProperty()
  packaging = db.StringProperty()
  label_condition = db.StringProperty()
  link = db.StringProperty()
  is_new = db.BooleanProperty()
  price_per_bottle = db.FloatProperty()
