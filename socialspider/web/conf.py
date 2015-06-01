# Copyright 2013-2014 Flavio Garcia
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


def get_component_config_file():
    """ The configuration file used on the administrator component is
        web.ini. """
    return "web.ini"


def parse_component_config(config):
    """ Basic configuration used by the admin component is:"""
    web_config = {
        'table_prefix': 's2',
        'connection_instance': 's2platform',
        'colony': None,
        'web': {
            'name': None,
            'nick': None
        }
    }
    if config.has_section('Colony'):
        web_config['colony'] = config.get('Colony', 'colony')
    if config.has_section('Web'):
        web_config['web']['name'] = config.get('Web', 'web.name')
        web_config['web']['nick'] = config.get('Web', 'web.nick')
    return web_config
