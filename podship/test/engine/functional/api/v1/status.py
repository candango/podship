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

from __future__ import (absolute_import, division, print_function,
                        with_statement)


import unittest
from tornado import httpclient
import logging
from tornado.escape import json_decode
import datetime
from ..v1 import api_url_v1

logger = logging.getLogger(__name__)


class StatusApiV1FunctionalTestCase(unittest.TestCase):
    """ Case that covers the account service.
    """

    def test_ping(self):
        http_client = httpclient.HTTPClient()
        ping_url = "%s/status/ping" % api_url_v1
        response_body = None
        try:
            response = http_client.fetch(httpclient.HTTPRequest(
                    url=ping_url, method='POST', body='ping'))
            response_body = json_decode(response.body)
            logger.error(response_body)
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            logger.error("Error: %s" % str(e))
        except Exception as e:
            # Other errors are possible, such as IOError.
            logger.error("Error: %s" % str(e))
        http_client.close()
        # Has pong
        self.assertEquals(response_body['data'], 'Pong')
        # Has a valid date
        self.assertTrue(datetime.datetime.strptime(
                response_body['date'], '%Y-%m-%d %H:%M:%S'))
