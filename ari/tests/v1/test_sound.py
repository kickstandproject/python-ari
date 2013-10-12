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
from ari.v1 import sound

SOUND = {
    'id': 'tt-monkeys',
    'text': '[sound of monkeys screaming]',
    'formats': [
        {
            'language': 'en',
            'format': 'gsm',
        },
    ],
}

FIXTURES = {
    '/sounds': {
        'GET': (
            {},
            [SOUND],
        ),
    },
    '/sounds/%s' % SOUND['id']: {
        'GET': (
            {},
            SOUND,
        ),
    },
}


class SoundManagerTest(testtools.TestCase):

    def setUp(self):
        super(SoundManagerTest, self).setUp()
        self.api = utils.FakeAPI(FIXTURES)
        self.manager = sound.SoundManager(self.api)

    def test_list(self):
        res = self.manager.list()
        expect = [
            ('GET', '/sounds', {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(len(res), 1)

    def test_show(self):
        res = self.manager.get(SOUND['id'])
        expect = [
            ('GET', '/sounds/%s' % SOUND['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res.id, SOUND['id'])
