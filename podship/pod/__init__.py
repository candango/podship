#!/usr/bin/env python
#
# Copyright 2015-2016 Flavio Garcia
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

from firenado.config import load_yaml_config_file
import firenado.tornadoweb
from podship.pod import handlers
import os
from tornado import httpclient
import tornado.ioloop
import logging


logger = logging.getLogger(__name__)


class PodComponent(firenado.tornadoweb.TornadoComponent):

    def __init__(self, name, application):
        super(PodComponent, self).__init__(name, application)
        self.ping_engine = None
        self.security_conf = None
        self.master_gateway_available = False
        self.project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..'))
        self.gateways = {}

    def get_handlers(self):
        return [
            (r'/', handlers.IndexHandler),
            (r'/locales/([A-Za-z0-9-_]+).json?', handlers.LocaleHandler),
            (r'/stream', handlers.StreamHandler),
        ]

    def initialize(self):
        logger.info('Initializing pod component')
        self.security_conf = load_yaml_config_file(
            os.path.join(self.project_root, 'conf', 'security.yml'))
        gateway_conf = load_yaml_config_file(
            os.path.join(self.project_root, 'conf', 'engine.yml'))
        print(gateway_conf)
        master_gateway = gateway_conf['gateway']['master']
        for instance in gateway_conf['gateway']['instances']:
            if master_gateway == instance['name']:
                self.gateways['master'] = instance
            self.gateways[instance['name']] = instance
        self.ping_engine = tornado.ioloop.PeriodicCallback(
                self.ping_engine_callback, 30000)
        self.ping_engine_callback()
        logger.info('Pod component initialized')

    def get_gateway_url(self, name):
        gateway = self.gateways[name]
        return 'http://%s:%s' % (gateway['host'], gateway['port'])

    def ping_engine_callback(self):
        from tornado import escape
        logger.debug('Pinging engine')
        self.ping_engine.stop()
        http_client = httpclient.HTTPClient()
        gateway_url = '%s/api/v1/status/%s' % (
            self.get_gateway_url('master'), 'ping')

        # TODO: get data from the config file
        data = escape.json_encode({'host': 'pod.candango.org', 'port': '8006'})

        try:
            response = http_client.fetch(httpclient.HTTPRequest(
                    url=gateway_url, method='POST', body=data))
            print(response.body)
            self.master_gateway_available = True
            logger.debug("Master gateway_url is available")
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            logger.error("Error: %s" % str(e))
            self.master_gateway_available = False
        except Exception as e:
            # Other errors are possible, such as IOError.
            logger.error("Error: %s" % str(e))
            http_client.close()
            self.master_gateway_available = False
        self.ping_engine.start()

    def shutdown(self):
        self.master_gateway_available = False
        logger.info('Shutting down pod component')
        self.ping_engine.stop()
        logger.info('Pod component shutdown')

    def install(self):
        from firenado.util.sqlalchemy_util import Base
        import podship.models
        print('Installing Diasporapy Pod...')
        print('Creating Pod ...')
        engine = self.application.get_data_source(
            'pod').get_connection()['engine']
        engine.echo = True
        # Dropping all
        # TODO Not to drop all if something is installed right?
        Base.metadata.drop_all(engine)
        # Creating database
        Base.metadata.create_all(engine)
