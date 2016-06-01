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
import pika
import os
import logging

from pika.adapters.tornado_connection import TornadoConnection


logger = logging.getLogger(__name__)

EXCHANGE_NAME = 'gateway_in'
INPUT_QUEUE_NAME = 'gateway_in_queue'


class EngineComponent(firenado.tornadoweb.TornadoComponent):

    def __init__(self, name, application):
        super(EngineComponent, self).__init__(name, application)
        self.processes = {}
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
        config = load_yaml_config_file(os.path.join(
            self.project_root, 'conf', 'engine.yml'))
        processes = int(config['processes'])
        logger.info("Starting engine.")
        for i in range(0, processes):
            logger.info("Spawning process #%s" % i)
        logger.info("Engine started.")

    def shutdown(self):
        pass

    def spawn_processes(self):
        pass


if __name__ == '__main__':
    import firenado.conf
    from firenado.core import TornadoApplication

    app = TornadoApplication()
    app.components['pod'].install()
