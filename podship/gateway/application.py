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

from . import handlers
from ..queue import RabbitMQClient
import os
import logging


logger = logging.getLogger(__name__)


class GatewayComponent(firenado.tornadoweb.TornadoComponent):

    def __init__(self, name, application):
        super(GatewayComponent, self).__init__(name, application)
        self.rabbitmq = {}
        self.rabbitmq['client'] = None
        self.project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..'))

    def get_handlers(self):
        return [
            (r'/', handlers.IndexHandler),
            (r'/stream', handlers.StreamHandler),
        ]

    # TODO: This method is just here to trigger the initialize method
    # Bug was raised on Firenado. Remove it when the bug get fixed.
    def get_config_filename(self):
        return 'engine'

    def initialize(self):
        self.rabbitmq['client'] = RabbitMQClient(
            load_yaml_config_file(os.path.join(
                self.project_root, 'conf', 'rabbitmq.yml')))
        self.rabbitmq['client'].connect()

    def shutdown(self):
        self.rabbitmq['client'].disconnect()


if __name__ == '__main__':
    import firenado.conf
    from firenado.tornadoweb import TornadoApplication

    app = TornadoApplication()
    app.components['pod'].install()
