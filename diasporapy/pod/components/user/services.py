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

from firenado.core.service import FirenadoService

from diasporapy.models import UserBase


class RegisterService(FirenadoService):

    def register(self):
        pass


class UserService(FirenadoService):

    def get_message(self, message):
        return 'The message is: %s' % message

    def create(self, data):
        user = UserBase()
        user.username = data['username']
        user.serialized_private_key = self.generate_serialized_private_key()
        user.language = data['language']
        user.email = data['email']
        user.encrypted_password = data['email']

    def generate_serialized_private_key(self):
        return ''

    def get_all(self):
        return []

    def by_id(self, id):
        return None
