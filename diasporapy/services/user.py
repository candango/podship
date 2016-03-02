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

from Crypto.PublicKey import RSA
import datetime
from diasporapy.models import UserBase
from firenado.conf import load_yaml_config_file
from firenado.core import service
from firenado.util import random_string
from passlib.hash import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import os


class UserService(service.FirenadoService):

    def __init__(self, handler, data_source=None):
        super(UserService, self).__init__(handler, data_source)
        #self.security = load_yaml_config_file()
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
        self.security_conf = load_yaml_config_file(
            os.path.join(self.project_root, 'conf', 'security.yml'))

    def create(self, user_data, created_utc=None, db_session=None):
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
        user.encrypted_password = bcrypt.encrypt(
            self.get_peppered_password(user_data['password']))
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
        if not db_session:
            db_session = self.get_data_source(
                'diasporapy').get_connection()['session']
            commit = True
        db_session.add(user)
        if commit:
            db_session.commit()
        return user

    def get_by_user_name(self, user_name, db_session=None):
        if not db_session:
            db_session = self.get_data_source(
                'diasporapy').get_connection()['session']
        auth_user = None
        try:
            auth_user = db_session.query(UserBase).filter(
                UserBase.user_name == user_name).one()
        except NoResultFound:
            pass
        return auth_user

    def is_password_valid(self, challenge, encrypted_password):
        return bcrypt.verify(
            self.get_peppered_password(challenge), encrypted_password)

    def get_peppered_password(self, password):
        return '%s%s' % (password, self.security_conf['password']['pepper'])

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
