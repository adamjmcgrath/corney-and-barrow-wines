#!/usr/bin/env python2.5
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext import deferred
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import tasks
import views


def main():
  application = webapp.WSGIApplication([
      ('/', views.ShowWines),
      ('/wine/(.+)', views.Wine),
      ('/sendemail', views.SendEmail),
      ('/getwines', tasks.GetWines),
  ],debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
