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

from firenado.config import load_yaml_config_file
import firenado.tornadoweb


import os
import logging
import tornado
from . import handlers


logger = logging.getLogger(__name__)


class PlatformTestComponent(firenado.tornadoweb.TornadoComponent):

    def get_handlers(self):
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')
        return [
            (r'/', handlers.IndexHandler),
            (r'/assets/(.*)', tornado.web.StaticFileHandler,
             {'path': assets_path}),
        ]
