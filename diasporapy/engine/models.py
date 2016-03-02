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

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Date, Integer, Text, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Index, DefaultClause
from sqlalchemy.dialects.postgres import TIMESTAMP

from firenado.util.sqlalchemy_util import Base


class EngineBase(Base):

    __tablename__ = 'engines'

    id = Column('id', Integer(), primary_key=True)
    host = Column('diaspora_handle', String(255), nullable=False)
    priority = Column('person_id', Integer(), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)


class PodBase(Base):

    __tablename__ = 'pods'

    id = Column('id', Integer(), primary_key=True)
    host = Column('host', String(255), nullable=True)
    ssl = Column('ssl', Boolean(), nullable=True)
    engine_id = Column('engine_id', Integer(), nullable=False)
    created_at = Column('created_at', TIMESTAMP(), nullable=False)
    updated_at = Column('updated_at', TIMESTAMP(), nullable=False)
    status = Column('status', Integer(), DefaultClause('0'), nullable=True)
    checked_at = Column('updated_at', TIMESTAMP(), nullable=False)
    offline_since = Column('updated_at', TIMESTAMP(), nullable=False)
    response_time = Column('response_time', Integer(), DefaultClause('-1'),
                           nullable=True)
    software = Column('software', String(255), nullable=True)
    error = Column('error', String(255), nullable=True)

Index('idx_pods_host', PodBase.host, unique=True, postgresql_using='btree')
Index('idx_pods_checked_at', PodBase.checked_at, postgresql_using='btree')
Index('idx_pods_offline_since', PodBase.offline_since,
      postgresql_using='btree')
Index('idx_pods_response_time', PodBase.response_time,
      postgresql_using='btree')
