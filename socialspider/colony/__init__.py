#!/usr/bin/env python
#
# Copyright 2015 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

from iflux.core import IfluxComponent
import tornado.web
import os

from socialspider.colony.handlers import IndexHandler


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
        if 'colonies' in self.config:
            self.colonies = self.config['colonies']
        if 'webs' in self.config:
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
        created_utc = datetime.datetime.utcnow()
        base_colony.uuid = str(uuid.uuid5(
            uuid.NAMESPACE_URL, '%s/%s' % (
                self.colonies['base']['domain'],
                created_utc))).replace('-', '')
        base_colony.name = self.colonies['base']['name']
        base_colony.nick = self.colonies['base']['nick']
        base_colony.domain = self.colonies['base']['domain']
        base_colony.created_at = created_utc
        base_colony.updated_at = created_utc

        session.add(base_colony)


        base_web = colony_models.WebBase()
        base_web.uuid = base_colony.uuid
        base_web.name = self.webs['default']['name']
        base_web.nick = self.webs['default']['nick']
        base_web.domain = self.colonies['base']['domain']
        base_web.colony_uuid = base_colony.uuid
        base_web.created_at = created_utc
        base_web.updated_at = created_utc

        session.add(base_web)

        session.commit()

        print 'Colony %s created at %s' % (
            base_colony.name, base_colony.created_at)

    def __get_connection_handler(self):
        return self.application.get_connection_handler(
            self.config['connection_instance']
        )
