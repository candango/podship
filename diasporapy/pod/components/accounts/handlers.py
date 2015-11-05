#!/usr/bin/env python
#
# Copyright 2015 Flavio Garcia
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
#
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

import firenado.core
from firenado.core.service import served_by

from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms_tornado import Form

import six


class LoginForm(Form):

    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])


class LoginHandler(firenado.core.TornadoHandler):

    @served_by('diasporapy.pod.components.accounts.services.AccountsService')
    def get(self):
        self.render('pod:accounts/login.html',
                    message=self.accounts_service.get_message('User Login'))

    def post(self):
        form = LoginForm(self.request.arguments)
        error_data = {}
        error_data['errors'] = {}
        if form.validate():
            print(form.data)
        else:
            self.set_status(401)
            error_data['errors'].update(form.errors)
            self.write(error_data)


class RegisterHandler(firenado.core.TornadoHandler):

    def get(self):
        self.render('pod:accounts/register.html')
