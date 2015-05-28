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

from sqlalchemy import Column, String
from sqlalchemy.types import DateTime

from iflux.util.sqlalchemy_util import Base


class ColonyBase(Base):

    __tablename__ = 's2_colonies'

    mysql_engine = 'MyISAM'
    mysql_charset = 'utf8'

    uuid = Column('uuid', String(36), primary_key=True)
    name = Column('name', String(255), nullable=False)
    nick = Column('nick', String(255), nullable=False)
    domain = Column('domain', String(255), nullable=False)
    created_at = Column('created_at', DateTime,
                     nullable=False, server_default='0000-00-00 00:00:00')
    updated_at = Column('updated_at', DateTime,
                     nullable=False, server_default='0000-00-00 00:00:00')
