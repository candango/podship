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
import uuid


class PersonService(service.FirenadoService):

    def create(self, person_data, created_utc=None, db_session=None):
        if not created_utc:
            created_utc = datetime.datetime.utcnow()

        person = PersonBase()
        # TODO: It looks like the guid should be generated based on a random
        # string. This generation based on the timestamp is not correct and
        # should be fixed.
        person.guid = str(uuid.uuid5(uuid.NAMESPACE_URL, str(created_utc)))
        person.url = ''
        person.diaspora_handle = ''
        person.serialized_public_key = ''
        if person_data['user']:
            person.owner_id = person_data['user'].id
        person.created_at = created_utc
        person.updated_at = created_utc
        person.closed_account = False
        person.fetch_status = 0
        commit = False
        if not db_session:
            session = self.get_data_source('pod').get_connection()['session']
            commit = True
        db_session.add(person)
        if commit:
            db_session.commit()

        return person
