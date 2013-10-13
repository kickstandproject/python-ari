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
from ari.v1 import endpoint

ENDPOINT = {
    'technology': 'IAX2',
    'resource': 'demo',
    'state': 'unknown',
    'channel_ids': [],
}

FIXTURES = {
    '/endpoints': {
        'GET': (
            {},
            [ENDPOINT],
        ),
    },
}


class EndpointManagerTest(testtools.TestCase):

    def setUp(self):
        super(EndpointManagerTest, self).setUp()
        self.api = utils.FakeAPI(FIXTURES)
        self.manager = endpoint.EndpointManager(self.api)

    def test_list(self):
        res = self.manager.list()
        expect = [
            ('GET', '/endpoints', {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(len(res), 1)
