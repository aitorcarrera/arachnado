# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from tornado import web


class ApiHandler(web.RequestHandler):
    """ Base handler for JSON APIs """

    def prepare(self):
        if self.request.headers["Content-Type"].startswith("application/json"):
            self.json_args = json.loads(self.request.body)
            self.is_json = True
        else:
            self.json_args = None
            self.is_json = False
