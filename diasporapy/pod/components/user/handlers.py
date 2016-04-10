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
from firenado.service import served_by

from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms_tornado import Form

import six


class LoginForm(Form):

    username = StringField(validators=[DataRequired(
        'The user name is required.')])
    password = PasswordField(validators=[DataRequired(
        'Password is required.')])


class LoginHandler(firenado.tornadoweb.TornadoHandler):

    @served_by('diasporapy.pod.components.user.services.UserService')
    def get(self):
        self.render('pod:account/login.html',
                    message=self.user_service.get_message('User Login'))

    @served_by('diasporapy.pod.components.user.services.UserService')
    def post(self):
        form = LoginForm(self.request.arguments)
        error_data = {}
        error_data['errors'] = {}
        if form.validate():
            is_valid_login = self.user_service.is_login_valid(form.data)
            print(is_valid_login)
            if is_valid_login['status'] == 200:
                self.set_status(is_valid_login['status'])
                response = {'status': is_valid_login['status']}
                response['userid'] = is_valid_login['response']['userid']
                response['next_url'] = self.session.get('next_url')
                response['password'] = ''
                self.write(response)
            elif is_valid_login['status'] == 401:
                self.set_status(is_valid_login['status'])
                error_data['errors'] = is_valid_login['response']['errors']
                self.write(error_data)
        else:
            self.set_status(401)
            error_data['errors'].update(form.errors)
            self.write(error_data)


class SignupHandler(firenado.tornadoweb.TornadoHandler):

    def get(self):
        self.render('pod:account/register.html')
