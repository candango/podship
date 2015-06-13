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


def get_component_config_file():
    """ The configuration file used on the administrator component is
        web.ini. """
    return "colony.ini"


def parse_component_config(config):
    """ Basic configuration used by the admin component is:"""
    colony_config = {
        'table_prefix': 's2',
        'connection_instance': 's2platform',
        'colonies': {},
        'webs': {}
    }
    if config.has_section('Colony'):
        if config.has_option('Colony', 'data.connection.instance'):
            colony_config['connection_instance'] = config.get(
                'Colony',
                'data.connection.instance'
            )
        colony_items = config.items('Colony')
        for key, value in colony_items:
            # Getting configured colonies
            if 'colonies.' in key:
                colony_x = key.split('.')
                if colony_x[1] not in colony_config['colonies']:
                    colony_config['colonies'][colony_x[1]] = {}
                colony_config['colonies'][colony_x[1]][colony_x[2]] = value
    if config.has_section('Web'):
        web_items = config.items('Web')
        for key, value in web_items:
            # Getting configured webs
            if 'webs.' in key:
                web_x = key.split('.')
                if web_x[1] not in colony_config['webs']:
                    colony_config['webs'][web_x[1]] = {}
                colony_config['webs'][web_x[1]][web_x[2]] = value
    return colony_config
