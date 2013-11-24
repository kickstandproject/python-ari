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
from ari.v1 import devicestate

DEVICESTATE = {
    'deviceName': 'statis:foo',
    'deviceState': 'RINGING',
}

UPDATE_DEVICESTATE = {
    'deviceName': 'statis:foo',
    'deviceState': 'BUSY',
}

FIXTURES = {
    '/deviceStates': {
        'GET': (
            {},
            [DEVICESTATE],
        ),
    },
    '/deviceStates/%s' % DEVICESTATE['deviceName']: {
        'DELETE': (
            {},
            None,
        ),
        'GET': (
            {},
            DEVICESTATE,
        ),
        'PUT': (
            {},
            DEVICESTATE,
        ),
    },
}


class DeviceStateManagerTest(testtools.TestCase):

    def setUp(self):
        super(DeviceStateManagerTest, self).setUp()
        self.api = utils.FakeAPI(FIXTURES)
        self.manager = devicestate.DeviceStateManager(self.api)

    def test_update(self):
        res = self.manager.update(
            device_state_id=UPDATE_DEVICESTATE['deviceName'],
            **UPDATE_DEVICESTATE)
        expect = [
            ('PUT', '/deviceStates/%s' % UPDATE_DEVICESTATE['deviceName'], {},
             UPDATE_DEVICESTATE),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)

    def test_delete(self):
        res = self.manager.delete(device_state_id=DEVICESTATE['deviceName'])
        expect = [
            ('DELETE', '/deviceStates/%s' % DEVICESTATE['deviceName'], {},
             None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_list(self):
        res = self.manager.list()
        expect = [
            ('GET', '/deviceStates', {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(len(res), 1)

    def test_show(self):
        res = self.manager.get(device_state_id=DEVICESTATE['deviceName'])
        expect = [
            ('GET', '/deviceStates/%s' % DEVICESTATE['deviceName'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res.deviceName, DEVICESTATE['deviceName'])
