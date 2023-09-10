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


# integration tests assume that the workflow in
# .github/workflows/tests-docker.yml has been executed

import requests

URL = 'http://localhost:5000'
TOPIC = 'admin'
TOPIC1 = 'oapi'
TOPIC2 = 'ui'
TOKEN = 'test_token'
TOKEN1 = 'token_1'
TOKEN2 = '2_test_token'


def test_no_auth():
    '''Test wis2box without authentication'''

    headers = {'X-Original-URI': f'/{TOPIC}', 'Authorization': 'Bearer'}
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers = {'X-Original-URI': f'/{TOPIC}?token={TOKEN}'}
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers = {
        'X-Original-URI': f'/{TOPIC}',
        'Authorization': f'Bearer {TOKEN}',
    }
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers = {
        'X-Original-URI': f'/oapi/collections/stations?token={TOKEN}',
        'X-api-http-method': 'GET'
    }
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers = {
        'X-Original-URI': f'/oapi/collections/stations?token={TOKEN}',
        'X-api-http-method': 'POST'
    }
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 401


def test_add_auth():
    '''Test adding wis2box authentication'''

    data = {'topic': TOPIC, 'token': TOKEN}
    r = requests.post(URL + '/add_token', data=data)
    assert r.status_code == 200

    data = {'topic': TOPIC1, 'token': TOKEN1}
    r = requests.post(URL + '/add_token', data=data)
    assert r.status_code == 200

    data = {'topic': TOPIC1, 'token': TOKEN2}
    r = requests.post(URL + '/add_token', data=data)
    assert r.status_code == 200


def test_header_auth():
    '''Test wis2box header authentication'''

    headers = {
        'X-Original-URI': f'/{TOPIC}',
        'Authorization': 'Bearer',
    }
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 401

    headers['X-Original-URI'] = f'/{TOPIC1}'
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 401

    headers['X-Original-URI'] = f'/{TOPIC2}'
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers = {
        'X-Original-URI': f'/{TOPIC}',
        'Authorization': f'Bearer {TOKEN}',
    }
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers['X-Original-URI'] = f'/{TOPIC1}'
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 401

    headers['X-Original-URI'] = f'/{TOPIC2}'
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200


def test_token_auth():
    '''Test wis2box token authentication'''

    headers = {
        'X-Original-URI': f'/{TOPIC}',
        'Authorization': 'Bearer',
    }
    r = requests.get(URL + '/authorize?token=', headers=headers)
    assert r.status_code == 401

    headers['X-Original-URI'] = f'/{TOPIC2}'
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers = {'X-Original-URI': f'/{TOPIC}?token={TOKEN}'}
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200

    headers = {'X-Original-URI': f'/{TOPIC1}?token={TOKEN1}'}
    r = requests.get(URL + '/authorize', headers=headers)
    assert r.status_code == 200


def test_remove_tokens():
    data = {'topic': TOPIC}
    r = requests.post(URL + '/remove_token', data=data)
    assert r.status_code == 200

    data = {'topic': TOPIC1}
    r = requests.post(URL + '/remove_token', data=data)
    assert r.status_code == 200
