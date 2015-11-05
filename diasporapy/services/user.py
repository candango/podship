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

from __future__ import (absolute_import, division, print_function,
                        with_statement)

from diasporapy.models import UserBase
from firenado.core import service
from firenado.util import random_string
import datetime
from sqlalchemy.orm.exc import NoResultFound
from Crypto.PublicKey import RSA


class UserService(service.FirenadoService):

    def create(self, user_data, created_utc=None, session=None):
        if not created_utc:
            created_utc = datetime.datetime.utcnow()

        user = UserBase()
        user.user_name = user_data['user_name']
        # TODO: Generate the serialized private key
        user.serialized_private_key = self.generate_key(user_data['password'])
        user.getting_started = True
        user.disable_mail = False
        # TODO: Handle language
        user.language = 'en'
        user.email = user_data['email']
        # TODO: encrypt the password
        user.encrypted_password = user_data['password']
        # Not used
        user.invitation_token = None
        user.invitation_sent_at = None
        user.reset_password_sent_at = None
        user.sign_in_count = 0
        user.current_sign_in_at = None
        user.last_sign_in_at = None
        user.current_sign_in_ip = None
        user.last_sign_in_ip = None
        user.created_at = created_utc
        user.updated_at = created_utc
        user.invitation_service = None
        user.invitation_identifier = None
        user.invitation_limit = None
        user.invited_by_id = None
        user.invited_by_type = None
        user.authentication_token = None
        user.unconfirmed_email = None
        user.confirm_email_token = None
        user.locked_at = None
        # TODO: This should be set based on an application settings
        user.show_community_spotlight_in_stream = True
        user.auto_follow_back = False
        user.auto_follow_back_aspect_id = None
        user.hidden_shareables = None
        user.reset_password_sent_at = None
        user.last_seen = None
        user.remove_after = None
        user.export = None
        user.exported_at = None
        user.exporting = False
        user.strip_exif = True
        user.exported_photos_file = None
        user.exported_photos_at = None
        user.exporting_photos = False

        commit = False
        if not session:
            session = self.get_data_source('pod').get_connection()['session']
            commit = True
        session.add(user)
        if commit:
            session.commit()

        return user

    def get_by_user_name(self, user_name):
        auth_user = None
        session = self.get_data_source('pod').get_connection()['session']
        try:
            auth_user = session.query(UserBase).filter(
                UserBase.user_name == user_name).one()
        except NoResultFound:
            pass
        return auth_user

    def generate_key(self, passphrase):
        """ FROM pyraspora: pyaspora.user.models
        Generate a 2048-bit RSA key. The key will be stored in the User
        object. The private key will be protected with password <passphrase>,
        which is usually the user password.
        """
        # TODO: I don't know if this is the way diaspora is handling the key
        # Let's keep this way by now
        # TODO: looks like this method is candidate to be part of some security
        # toolkit

        RSAkey = RSA.generate(2048)

        private_key = RSAkey.exportKey(
            format='PEM',
            pkcs=1,
            passphrase=passphrase
        ).decode("ascii")
        return RSAkey.publickey().exportKey(
            format='PEM',
            pkcs=1
        ).decode("ascii")
