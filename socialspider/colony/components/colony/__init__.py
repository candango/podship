from socialspider.colony.components.colony.handlers import IndexHandler
from iflux.core import IfluxComponent
import tornado.web
import os


class ColonyComponent(IfluxComponent):

    def __init__(self, name, application, config={}):
        IfluxComponent.__init__(self, name, application, config)
        self.db_backend = None
        self.colonies = {}
        self.webs = {}

    def get_handlers(self):
        handlers = [
            (r'/', IndexHandler),
            (r"/colony/static/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(), 'static')}),
        ]
        return handlers

    def process_config(self):
        self.colonies = self.config['colonies']
        self.webs = self.config['webs']
