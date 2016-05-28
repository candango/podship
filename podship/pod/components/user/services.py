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

from firenado.core.service import FirenadoService

from tornado import httpclient
import logging
from tornado.escape import json_decode, json_encode

logger = logging.getLogger(__name__)


class UserService(FirenadoService):

    def get_message(self, message):
        return 'The message is: %s' % message

    def is_login_valid(self, form_data):
        print(form_data)
        http_client = httpclient.HTTPClient()
        login_url = "http://localhost:8007/api/v1/user/login"
        response_body = None
        code = 0
        data = {
            'payload': form_data
        }
        try:
            response = http_client.fetch(httpclient.HTTPRequest(
                    url=login_url, method='POST', body=json_encode(data)))
            code = response.code
            response_body = json_decode(response.body)
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            logger.debug("Error: %s" % str(e))
            code = e.response.code
            response_body = json_decode(e.response.body)
        except Exception as e:
            # Other errors are possible, such as IOError.
            logger.error("Error: %s" % str(e))
        http_client.close()
        return {
            'status': code,
            'response': response_body
        }
