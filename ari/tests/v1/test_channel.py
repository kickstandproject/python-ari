# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools

from ari.tests import utils
from ari.v1 import channel

CHANNEL = {
    'id': '1381610401.13',
    'name': 'Local/s@demo-00000003;2',
    'state': 'Up',
    'caller': {
        'name': '',
        'number': '',
    },
    'connected': {
        'name': '',
        'number': '',
    },
    'accountcode': '',
    'dialplan': {
        'context': 'demo',
        'exten': 's',
        'priority': 5,
    },
    'creationtime': '2013-10-12T16:40:01.946-0400',
}

FIXTURES = {
    '/channels': {
        'GET': (
            {},
            [CHANNEL],
        ),
    },
    '/channels/%s' % CHANNEL['id']: {
        'GET': (
            {},
            CHANNEL,
        ),
        'DELETE': (
            {},
            None,
        ),
    },
}


class ChannelManagerTest(testtools.TestCase):

    def setUp(self):
        super(ChannelManagerTest, self).setUp()
        self.api = utils.FakeAPI(FIXTURES)
        self.manager = channel.ChannelManager(self.api)

    def test_list(self):
        res = self.manager.list()
        expect = [
            ('GET', '/channels', {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(len(res), 1)

    def test_show(self):
        res = self.manager.get(channel_id=CHANNEL['id'])
        expect = [
            ('GET', '/channels/%s' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res.id, CHANNEL['id'])

    def test_delete(self):
        res = self.manager.delete(channel_id=CHANNEL['id'])
        expect = [
            ('DELETE', '/channels/%s' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)
