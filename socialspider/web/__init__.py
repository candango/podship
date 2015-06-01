from iflux.core import IfluxComponent
import tornado.web
import os

from socialspider.web.handlers import IndexHandler


class WebComponent(IfluxComponent):

    def __init__(self, name, application, config={}):
        IfluxComponent.__init__(self, name, application, config)
        self.db_backend = None
        self.colony = None
        self.web = None

    def get_handlers(self):
        handlers = [
            (r'/', IndexHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(), '../static')}),
        ]
        return handlers

    def process_config(self):
        self.colony = self.config['colony']
        self.web = self.config['web']

    def __get_connection_handler(self):
        return self.application.get_connection_handler(
            self.config['connection_instance']
        )
