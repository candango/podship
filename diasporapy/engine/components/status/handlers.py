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

import firenado.tornadoweb
import logging
import datetime
import uuid
import pika
from tornado import gen
from tornado.locks import Condition


logger = logging.getLogger(__name__)


class PingHandler(firenado.tornadoweb.TornadoHandler):

    def __init__(self, application, request, **kwargs):
        super(PingHandler, self).__init__(application, request, **kwargs)
        self.callback_queue = None
        self.condition = Condition()
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.in_channel = self.application.get_app_component().rabbitmq[
            'client'].channels['in']

    @gen.coroutine
    def post(self):
        self.in_channel.queue_declare(exclusive=True,
                                      callback=self.on_request_queue_declared)
        yield self.condition.wait()

        self.write(self.response)

    def on_request_queue_declared(self, response):
        logger.info('Request temporary queue declared.')
        self.callback_queue = response.method.queue
        self.in_channel.basic_consume(self.on_response, no_ack=True,
                                      queue=self.callback_queue)
        self.in_channel.basic_publish(
            exchange='',
            routing_key='ping_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=self.request.body)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = {
                'data': body.decode("utf-8"),
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.in_channel.queue_delete(queue=self.callback_queue)
            self.condition.notify()