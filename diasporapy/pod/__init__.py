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

from diasporapy.pod import handlers
import firenado.core
import tornado.web
import os


class PodComponent(firenado.core.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/', handlers.IndexHandler),
            (r'/stream', handlers.StreamHandler),
            (r"/assets/bootstrap/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(), '..',
                                   'bower_components', 'bootstrap', 'dist')}),
            (r"/assets/canjs/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(), '..',
                                   'bower_components', 'canjs')}),
            (r"/assets/jquery/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(), '..',
                                   'bower_components', 'jquery', 'dist')}),
            (r"/assets/i18next/(.*)", tornado.web.StaticFileHandler,
             {"path": os.path.join(self.get_component_path(), '..',
                                   'bower_components', 'i18next')}),
        ]

    def install(self):
        import diasporapy.pod.models as models
        from firenado.util.sqlalchemy_util import Base
        import uuid
        import datetime

        print 'Installing Diasporapy Pod...'

        print 'Creating Pod ...'

        print self.application.get_data_source('pod').get_connection()

        engine = self.application.get_data_source('pod').get_connection()['engine']
        engine.echo = True

        # Dropping all
        # TODO Not to drop all if something is installed right?
        Base.metadata.drop_all(engine)
        # Creating database
        Base.metadata.create_all(engine)

        #session = self.__get_connection_handler().get_connection()['session']

        #session.commit()

        #print 'Colony %s created at %s' % (
            #base_colony.name, base_colony.created_at)


if __name__ == '__main__':
    import firenado.conf
    from firenado.core import TornadoApplication

    app = TornadoApplication()
    app.components['pod'].install()