# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import itertools
from tornado.web import Application, RequestHandler, url

from .spider import get_crawler
from .monitor import Monitor
from .api import ApiHandler

at_root = lambda *args: os.path.join(os.path.dirname(__file__), *args)


def get_application(crawler_process):
    handlers = [
        url(r"/", Index, name="index"),
        url(r"/help", Help, name="help"),
        url(r"/settings", Settings, name="settings"),
        url(r"/start", StartCrawler, {'crawler_process': crawler_process}, name="start"),
        url(r"/ws", Monitor, {'crawler_process': crawler_process}, name="ws"),
    ]
    return Application(
        handlers=handlers,
        template_path=at_root("templates"),
        compiled_template_cache=False,
        static_path=at_root("static"),
        # no_keep_alive=True,
        compress_response=True,
    )


class Index(RequestHandler):
    def get(self):
        return self.render("index.html")


class Help(RequestHandler):
    def get(self):
        return self.render("help.html")


class Settings(RequestHandler):
    def get(self):
        return self.render("settings.html")


class StartCrawler(ApiHandler, RequestHandler):
    """
    This endpoint starts crawling for a domain.
    """
    crawl_ids = itertools.count(1)

    def initialize(self, crawler_process):
        self.crawler_process = crawler_process

    def crawl(self, domain):
        crawler = get_crawler()
        crawl_id = next(self.crawl_ids)
        self.crawler_process.crawl(crawler, domain=domain, crawl_id=crawl_id)

    def post(self):
        if self.is_json:
            domain = self.json_args['domain']
            self.crawl(domain)
            return {"status": "ok"}
        else:
            domain = self.get_body_argument('domain')
            self.crawl(domain)
            self.redirect("/")