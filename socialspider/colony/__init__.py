from iflux.core import IfluxComponent
import tornado.web
import os

from colony.handlers import IndexHandler


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

    def install(self):
        import socialspider.colony.models as colony_models
        from iflux.util.sqlalchemy_util import Base
        import uuid
        import datetime

        print 'Installing Colony Application...'

        print 'Creating base Colony ...'

        engine = self.__get_connection_handler().get_connection()['engine']
        engine.echo=True

        # Dropping all
        # TODO Not to drop all if something is installed right?
        Base.metadata.drop_all(engine)
        # Creating database
        Base.metadata.create_all(engine)

        session = self.__get_connection_handler().get_connection()['session']

        # Creating colony
        base_colony = colony_models.ColonyBase()
        base_colony.uuid = str(uuid.uuid5(
            uuid.NAMESPACE_DNS, self.colonies['base']['domain']))
        base_colony.name = self.colonies['base']['name']
        base_colony.nick = self.colonies['base']['nick']
        base_colony.domain = self.colonies['base']['domain']
        base_colony.created_at = datetime.datetime.utcnow()
        base_colony.updated_at = datetime.datetime.utcnow()

        session.add(base_colony)

        session.commit()

        print 'Colony %s created at %s' % (
            base_colony.name, base_colony.created_at)

    def __get_connection_handler(self):
        return self.application.get_connection_handler(
            self.config['connection_instance']
        )
        self.webs = self.config['webs']
