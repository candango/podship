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
from tornado.escape import json_decode, json_encode
from ..v1 import api_url_v1

logger = logging.getLogger(__name__)


class UserApiV1FunctionalTestCase(unittest.TestCase):
    """ Case that covers the account service.
    """

    def test_login_empty_body(self):
        http_client = httpclient.HTTPClient()
        login_url = "%s/user/login" % api_url_v1
        response_body = None
        error_code = 0
        body_error_code = 0
        try:
            http_client.fetch(httpclient.HTTPRequest(
                    url=login_url, method='POST', body=''))
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            response_body = json_decode(e.response.body)
            error_code = e.code
            body_error_code = int(response_body['status'])
            print(e.response.error)
        except Exception as e:
            # Other errors are possible, such as IOError.
            logger.error("Error: %s" % str(e))
        http_client.close()
        # Bad Request http error
        self.assertEquals(error_code, 500)
        self.assertEquals(body_error_code, 500)
        # Has 1 error
        self.assertEquals(len(response_body['errors']), 1)
        # Username message
        self.assertEquals(response_body['errors']['schema'][0],
                          "Invalid body content.")

    def test_login_invalid_json(self):
        http_client = httpclient.HTTPClient()
        login_url = "%s/user/login" % api_url_v1
        response_body = None
        data = "invalid json string"
        error_code = 0
        body_error_code = 0
        try:
            http_client.fetch(httpclient.HTTPRequest(
                    url=login_url, method='POST', body=''))
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            response_body = json_decode(e.response.body)
            error_code = e.code
            body_error_code = int(response_body['status'])
            print(e.response.error)
        except Exception as e:
            # Other errors are possible, such as IOError.
            logger.error("Error: %s" % str(e))
        http_client.close()
        # Bad Request http error
        self.assertEquals(error_code, 500)
        self.assertEquals(body_error_code, 500)
        # Has 1 error
        self.assertEquals(len(response_body['errors']), 1)
        # Username message
        self.assertEquals(response_body['errors']['schema'][0],
                          "Invalid body content.")

    def test_login_without_username_password(self):
        http_client = httpclient.HTTPClient()
        login_url = "%s/user/login" % api_url_v1
        response_body = None
        error_code = 0

        data = {
            'payload': {
                'username': "",
                'password': "",
            }
        }

        try:
            response = http_client.fetch(httpclient.HTTPRequest(
                    url=login_url, method='POST', body=json_encode(data)))
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            logger.error("Error: %s" % str(e))
            error_code = e.code
            response_body = json_decode(e.response.body)
        except Exception as e:
            # Other errors are possible, such as IOError.
            logger.error("Error: %s" % str(e))
        http_client.close()
        # Unauthorized http error
        self.assertEquals(error_code, 400)
        # Has 2 errors
        self.assertEquals(len(response_body['errors']), 1)
        # Username message
        self.assertTrue(response_body['errors']['schema'],
                        "The user name is required.")
        # Password message
        self.assertTrue(response_body['errors']['password'],
                        "Password is required.")
