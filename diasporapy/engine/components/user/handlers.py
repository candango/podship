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

import firenado.core
from firenado.core.service import served_by
import logging
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from tornado.escape import json_decode

from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms_tornado import Form
import wtforms_json

wtforms_json.init()

# TODO: Use this instead of wtforms
# https://pypi.python.org/pypi/jsonschema

import six

# Schema definition from:
# http://spacetelescope.github.io/understanding-json-schema/structuring.html
schema = {
    "type": "object",
    "properties": {
        "payload": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["username", "password"],
        },
    },
    "required": ["payload"],
}

# Schema error should be 400


class LoginForm(Form):

    username = StringField(validators=[DataRequired(
        'The user name is required.')])
    password = PasswordField(validators=[DataRequired(
        'Password is required.')])

logger = logging.getLogger(__name__)


class LoginHandler(firenado.core.TornadoHandler):

    @served_by('diasporapy.services.account.AccountService')
    def post(self):
        data = None
        try:
            data = json_decode(self.request.body)
            try:
                validate(data, schema)
                form = LoginForm.from_json(data['payload'])
                error_data = {}
                error_data['errors'] = {}
                if form.validate():
                    is_valid_login = self.account_service.is_login_valid(form.data)
                    if is_valid_login:
                        response = {'status': 200}
                        response['userid'] = is_valid_login.id
                        print(response)
                        self.write(response)
                    else:
                        self.set_status(401)
                        error_data['errors']['form'] = ['Invalid Login']
                        self.write(error_data)
                else:
                    self.set_status(401)
                    error_data['errors'].update(form.errors)
                    self.write(error_data)
            except ValidationError as e:
                self.set_status(400)
                response = {'status': 400}
                response['errors'] = {
                    'schema': e.message
                }
                self.write(response)
        except ValueError as e:
            self.set_status(500)
            response = {'status': 500}
            response['errors'] = {
                'schema': ["Invalid json body content."]
            }
            self.write(response)

    def get_data_sources(self):
        return self.get_data_connected().data_sources