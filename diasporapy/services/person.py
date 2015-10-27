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
from diasporapy.models import PersonBase
from firenado.core import service


class PersonService(service.FirenadoService):

    def create(self, person_data):
        person = PersonBase()
        person.guid = ''
        person.url = ''
        person.diaspora_handle = ''
        person.serialized_public_key = ''
        if person_data['user']:
            person.owner_id = person_data['user'].id
        person.created_at = datetime.datetime.utcnow()
        person.updated_at = datetime.datetime.utcnow()
        person.closed_account = False
        person.fetch_status = 0

        session = self.get_data_source('pod').get_connection()['session']
        session.add(person)
        session.commit()

        return person
