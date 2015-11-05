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

from diasporapy.services.account import AccountService
import firenado.conf
import firenado.core
from firenado.core.service import served_by
import os

# Setting pod dir
test_dirname, filename = os.path.split(os.path.abspath(__file__))
DIASPORAPY_POD_DIR = os.path.join(test_dirname, '..', 'pod')
os.environ["FIRENADO_CURRENT_APP_CONFIG_PATH"] = os.path.join(
    DIASPORAPY_POD_DIR, 'conf')
#Reloading firenaod.conf so it loads the pod config files
reload(firenado.conf)

application = firenado.core.TornadoApplication()


class DevSetupExec:

    def __init__(self, application):
        self.application = application

    @served_by(AccountService)
    def create_accounts(self):
        account_data = {}
        account_data['user_data'] = {
            'user_name': 'test',
            'email': 'test@test.ts',
            'password': 'test',
        }

        self.account_service.register(account_data)


dev_setup_exec = DevSetupExec(application)
dev_setup_exec.create_accounts()

