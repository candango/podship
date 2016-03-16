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

from firenado.conf import load_yaml_config_file
import firenado.core

from . import handlers
import pika
import os
import logging

from pika.adapters.tornado_connection import TornadoConnection


logger = logging.getLogger(__name__)


# Based on https://gist.github.com/brimcfadden/2855520
class RabbitMQClient(object):

    def __init__(self):
        self.connecting = False
        self.connection = None
        self.channel = None
        self.in_channel = None
        self.out_channels = {}

    def connect(self):
        if self.connecting:
            pika.log.info('Already connecting to RabbitMQ')
            return
        pika.log.info("Connecting to RabbitMQ")
        self.connecting = True

EXCHANGE_NAME = 'gateway_in'

INPUT_QUEUE_NAME = 'gateway_in_queue'

class EngineComponent(firenado.core.TornadoComponent):

    def __init__(self, name, application):
        super(EngineComponent, self).__init__(name, application)
        self.rabbitmq = {}
        self.rabbitmq['channels'] = {}
        self.rabbitmq['channels']['in'] = None
        self.rabbitmq['channels']['out'] = {}
        self.rabbitmq['conf'] = None
        self.rabbitmq['connecting'] = False
        self.rabbitmq['connection'] = None
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
        self.rabbitmq['conf'] = load_yaml_config_file(
            os.path.join(self.project_root, 'conf', 'rabbitmq.yml'))
        logger.info('Initializing engine component')

        logger.info("Connecting to RabbitMQ")

        self.rabbitmq['connecting'] = True

        creds = pika.PlainCredentials(
            self.rabbitmq['conf']['user'],
            self.rabbitmq['conf']['pass']
        )
        params = pika.ConnectionParameters(
            host=self.rabbitmq['conf']['host'],
            port=self.rabbitmq['conf']['port'],
            virtual_host='/',
            credentials=creds
        )

        TornadoConnection(
            params,
            on_open_callback=self.rabbitmq_connection_opened,
            on_close_callback=self.rabbitmq_connection_closed,
            on_open_error_callback=self.rabbitmq_connection_failed
        )

    def shutdown(self):
        self.rabbitmq['connection'].close()

    def rabbitmq_connection_opened(self, connection):
        logger.info('Engine connected to RabbitMQ')
        self.rabbitmq['connection'] = connection
        self.rabbitmq['connection'].channel(self.rabbitmq_channel_opened)

    def rabbitmq_channel_opened(self, channel):
        logger.info('Engine channel opened with RabbitMQ')
        self.rabbitmq['channels']['in'] = channel
        self.rabbitmq['channels']['in'].exchange_declare(
            exchange=EXCHANGE_NAME,
            type='topic')
        self.rabbitmq['channels']['in'].queue_declare(
            callback=self.rabbitmq_input_queue_declared,
            queue=INPUT_QUEUE_NAME)
        logger.info('Engine component initialized')

    def rabbitmq_input_queue_declared(self, queue):
        logger.info('Engine input queue declared on RabbitMQ')
        self.rabbitmq['channels']['in'].queue_bind(callback=None,
                                                   exchange=EXCHANGE_NAME,
                                                   queue=INPUT_QUEUE_NAME,
                                                   routing_key="#")

    def rabbitmq_connection_closed(self, connection, code, message):
        logger.info('Engine disconnected from RabbitMQ')

    def rabbitmq_connection_failed(self, connection, error_message):
        logger.error('Engine was no able to connect to RabbitMQ, '
                     'terminating the node. Cause: %s' % error_message)
        import tornado.ioloop
        tornado.ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    import firenado.conf
    from firenado.core import TornadoApplication

    app = TornadoApplication()
    app.components['pod'].install()
