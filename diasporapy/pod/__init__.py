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

import firenado.core
import tornado.web
import os

from diasporapy.pod import handlers


class PodComponent(firenado.core.TornadoComponent):

    def get_handlers(self):
        return [
            (r'/', handlers.IndexHandler),
            (r'/locales/([A-Za-z0-9-_]+).json?', handlers.LocaleHandler),
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
        from firenado.util.sqlalchemy_util import Base
        import diasporapy.models

        print 'Installing Diasporapy Pod...'

        print 'Creating Pod ...'

        engine = self.application.get_data_source(
            'pod').get_connection()['engine']
        engine.echo = True

        # Dropping all
        # TODO Not to drop all if something is installed right?
        Base.metadata.drop_all(engine)
        # Creating database
        Base.metadata.create_all(engine)


if __name__ == '__main__':
    import firenado.conf
    from firenado.core import TornadoApplication

    app = TornadoApplication()
    app.components['pod'].install()
