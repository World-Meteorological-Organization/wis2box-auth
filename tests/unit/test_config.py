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

from wis2box_auth import (
    is_token_authorized,
    is_resource_open,
    create_token,
    delete_token,
    extract_topic,
)

TOPIC = 'admin'
TOPIC1 = TOPIC + '1'
TOPIC2 = TOPIC + '2'
TOKEN = 'test_token'
TOKEN1 = TOKEN + '1'
TOKEN2 = TOKEN + '2'


def test_create_token():

    assert is_resource_open(TOPIC) is True
    assert is_resource_open(TOPIC1) is True
    assert is_resource_open(TOPIC2) is True

    create_token(TOPIC, TOKEN)
    create_token(TOPIC1, TOKEN1)
    create_token(TOPIC1, TOKEN2)

    assert is_resource_open(TOPIC) is False
    assert is_resource_open(TOPIC1) is False
    assert is_resource_open(TOPIC2) is True

    assert is_token_authorized(TOPIC, TOKEN) is True
    assert is_token_authorized(TOPIC, TOKEN1) is False
    assert is_token_authorized(TOPIC, TOKEN2) is False
    assert is_token_authorized(TOPIC1, TOKEN) is False
    assert is_token_authorized(TOPIC1, TOKEN1) is True
    assert is_token_authorized(TOPIC1, TOKEN2) is True

    delete_token(TOPIC)
    delete_token(TOPIC1)


def test_delete_token():
    create_token(TOPIC, TOKEN)
    create_token(TOPIC1, TOKEN1)
    create_token(TOPIC1, TOKEN2)

    delete_token(TOPIC)
    assert is_resource_open(TOPIC) is True

    delete_token(TOPIC1, TOKEN1)
    assert is_token_authorized(TOPIC1, TOKEN1) is False
    assert is_token_authorized(TOPIC1, TOKEN2) is True

    delete_token(TOPIC1, TOKEN2)
    assert is_token_authorized(TOPIC1, TOKEN2) is False


def test_extract_token():
    create_token(TOPIC, TOKEN)

    topic = extract_topic(TOPIC1)
    assert TOPIC == topic

    delete_token(TOPIC)

    topic = extract_topic(TOPIC1)
    assert topic is None
