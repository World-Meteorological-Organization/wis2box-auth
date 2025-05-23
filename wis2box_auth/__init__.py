###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

__version__ = '1.1.dev0'

import logging
import os
from pathlib import Path

from wis2box_auth.base import BaseAuth

LOGGER = logging.getLogger(__name__)

if os.environ.get('WIS2BOX_AUTH_STORE'):
    AUTH_STORE = Path(os.environ.get('WIS2BOX_AUTH_STORE'))
else:
    AUTH_STORE = Path('/data/wis2box/auth.db')


def is_resource_open(topic: str) -> bool:
    """
    Checks if topic has access control configured

    :param topic: `str` topic hierarchy

    :returns: `bool` of result
    """

    auth_db = BaseAuth(AUTH_STORE)

    return auth_db.is_resource_open(topic)


def is_token_authorized(topic: str, token: str) -> bool:
    """
    Checks if token is authorized to access a topic

    :param topic: `str` topic hierarchy
    :param token: `str` auth token

    :returns: `bool` of result
    """

    auth_db = BaseAuth(AUTH_STORE)

    return auth_db.is_token_authorized(token, topic)


def create_token(topic: str, token: str) -> bool:
    """
    Add token to authentication database

    :param topic: `str` topic hierarchy
    :param token: `str` auth token

    :returns: `bool` of result
    """

    auth_db = BaseAuth(AUTH_STORE)

    auth_db.add(token, topic)
    return auth_db.is_token_authorized(token, topic)


def delete_token(topic: str, token: str = '') -> bool:
    """
    Add token to authentication database

    :param topic: `str` topic hierarchy
    :param token: `str` auth token

    :returns: `bool` of result
    """

    auth_db = BaseAuth(AUTH_STORE)

    if not token:
        LOGGER.debug(f'Deleting all tokens for topic {topic}')
        return auth_db.delete_by_topic_hierarchy(topic)
    else:
        LOGGER.debug(f'Deleting token {token} for topic {topic}')
        return auth_db.delete_by_token(token, topic)


def extract_topic(topic: str = None) -> bool:
    """
    Extrack token to from auth database

    :param topic: `str` topic hierarchy

    :returns: `str` of result
    """

    auth_db = BaseAuth(AUTH_STORE)

    LOGGER.debug(f'topic {topic}')

    if any([x in topic for x in ['processes', 'execution']]):
        LOGGER.debug('topic is an API process execution')
        sanitized_topic = topic
    elif any([x in topic for x in ['collections/stations', 'collections/discovery-metadata']]):  # noqa
        LOGGER.debug('topic is an API metadata transaction')
        sanitized_topic = topic
    else:
        sanitized_topic = topic.replace('/', '.')

    LOGGER.debug(f'sanitized topic {sanitized_topic}')

    return auth_db.extract_topic(sanitized_topic)
