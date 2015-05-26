from socialspider.colony.components.colony.handlers import IndexHandler
from iflux.core import IfluxComponent

class ColonyComponent(IfluxComponent):


    def get_handlers(self):
        handlers = [
            (r'/', IndexHandler),
        ]
        return handlers

