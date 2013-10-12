# -*- coding: utf-8 -*-
# Copyright (c) 2013 PolyBeacon, Inc.

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
from ari.v1 import bridge

BRIDGE = {
    'id': 'b5142338-d88a-403e-bb14-e1fba0a318d2',
    'technology': 'simple_bridge',
    'bridge_type': 'mixing',
    'bridge_class': 'base',
    'channels': [
    ],
}

CREATE_BRIDGE = {
    'type': 'mixing',
}

FIXTURES = {
    '/bridges': {
        'GET': (
            {},
            [BRIDGE],
        ),
        'POST': (
            {},
            BRIDGE,
        ),
    },
    '/bridges/%s' % BRIDGE['id']: {
        'GET': (
            {},
            BRIDGE,
        ),
        'DELETE': (
            {},
            None,
        ),
    },
}


class BridgeManagerTest(testtools.TestCase):

    def setUp(self):
        super(BridgeManagerTest, self).setUp()
        self.api = utils.FakeAPI(FIXTURES)
        self.manager = bridge.BridgeManager(self.api)

    def test_list(self):
        res = self.manager.list()
        expect = [
            ('GET', '/bridges', {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(len(res), 1)

    def test_show(self):
        res = self.manager.get(bridge_id=BRIDGE['id'])
        expect = [
            ('GET', '/bridges/%s' % BRIDGE['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res.id, BRIDGE['id'])

    def test_delete(self):
        res = self.manager.delete(bridge_id=BRIDGE['id'])
        expect = [
            ('DELETE', '/bridges/%s' % BRIDGE['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_create(self):
        res = self.manager.create(**CREATE_BRIDGE)
        expect = [
            ('POST', '/bridges', {}, CREATE_BRIDGE),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)
