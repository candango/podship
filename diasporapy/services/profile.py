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

import datetime
from diasporapy.models import ProfileBase
from firenado.core import service


class ProfileService(service.FirenadoService):

    def create(self, profile_data):
        """

        :param person:
        :param first_name:
        :param last_name:
        :return:
        """
        profile = ProfileBase()
        profile.first_name = profile_data['first_name']
        profile.last_name = profile_data['last_name']
        profile.image_url = ''
        profile.image_url_small = ''
        profile.image_url_medium = ''
        profile.birthday = None
        profile.gender = ''
        profile.bio = ''
        profile.searchable = True
        # TODO: this should be filled at the beginning
        profile.person_id = profile_data['person'].id
        profile.created_at = datetime.datetime.utcnow()
        profile.updated_at = datetime.datetime.utcnow()
        profile.location = ''
        profile.full_name = ''
        profile.nsfw = False

        session = self.get_data_source('pod').get_connection()['session']
        session.add(profile)
        session.commit()

        return profile
