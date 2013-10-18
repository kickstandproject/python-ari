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

CREATE_CHANNEL = {
    'app': 'foo',
    'appArgs': 'bar',
    'callerId': 'Bob',
    'context': 'demo',
    'endpoint': 'Local/s',
    'extension': 's',
    'priority': '1',
    'timeout': 30,
}

DIAL_CHANNEL = {
    'context': 'demo',
    'endpoint': 'Local/s',
    'extension': 's',
    'timeout': 30,
}

EXIT_CHANNEL = {
    'context': 'demo',
    'extension': 's',
    'priority': '1',
}

MUSIC_CHANNEL = {
    'mohClass': 'default',
}

MUTE_CHANNEL = {
    'direction': 'both',
}

PLAY_CHANNEL = {
    'media': 'sound:demo-congrats',
    'lang': 'en',
    'offsetms': '0',
    'skipms': '3000',
}

FIXTURES = {
    '/channels': {
        'GET': (
            {},
            [CHANNEL],
        ),
        'POST': (
            {},
            CREATE_CHANNEL,
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
    '/channels/%s/answer' % CHANNEL['id']: {
        'POST': (
            {},
            None,
        ),
    },
    '/channels/%s/continue' % CHANNEL['id']: {
        'POST': (
            {},
            None,
        ),
    },
    '/channels/%s/dial' % CHANNEL['id']: {
        'POST': (
            {},
            DIAL_CHANNEL,
        ),
    },
    '/channels/%s/hold' % CHANNEL['id']: {
        'DELETE': (
            {},
            None,
        ),
        'POST': (
            {},
            None,
        ),
    },
    '/channels/%s/moh' % CHANNEL['id']: {
        'DELETE': (
            {},
            None,
        ),
        'POST': (
            {},
            MUSIC_CHANNEL,
        ),
    },
    '/channels/%s/mute' % CHANNEL['id']: {
        'POST': (
            {},
            MUTE_CHANNEL,
        ),
    },
    '/channels/%s/play' % CHANNEL['id']: {
        'POST': (
            {},
            PLAY_CHANNEL,
        ),
    },
    '/channels/%s/unmute' % CHANNEL['id']: {
        'POST': (
            {},
            MUTE_CHANNEL,
        ),
    },
}


class ChannelManagerTest(testtools.TestCase):

    def setUp(self):
        super(ChannelManagerTest, self).setUp()
        self.api = utils.FakeAPI(FIXTURES)
        self.manager = channel.ChannelManager(self.api)

    def test_add_audio(self):
        res = self.manager.add_audio(channel_id=CHANNEL['id'], **PLAY_CHANNEL)
        expect = [
            ('POST', '/channels/%s/play' % CHANNEL['id'], {}, PLAY_CHANNEL),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)

    def test_add_music(self):
        res = self.manager.add_music(channel_id=CHANNEL['id'], **MUSIC_CHANNEL)
        expect = [
            ('POST', '/channels/%s/moh' % CHANNEL['id'], {}, MUSIC_CHANNEL),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)

    def test_answer(self):
        res = self.manager.answer(channel_id=CHANNEL['id'])
        expect = [
            ('POST', '/channels/%s/answer' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_create(self):
        res = self.manager.create(**CREATE_CHANNEL)
        expect = [
            ('POST', '/channels', {}, CREATE_CHANNEL),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)

    def test_delete(self):
        res = self.manager.delete(channel_id=CHANNEL['id'])
        expect = [
            ('DELETE', '/channels/%s' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_dial(self):
        res = self.manager.dial(channel_id=CHANNEL['id'], **DIAL_CHANNEL)
        expect = [
            ('POST', '/channels/%s/dial' % CHANNEL['id'], {}, DIAL_CHANNEL),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)

    def test_exit(self):
        res = self.manager.exit(
            channel_id=CHANNEL['id'], **EXIT_CHANNEL)
        expect = [
            (
                'POST', '/channels/%s/continue' % CHANNEL['id'], {},
                EXIT_CHANNEL),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_hold(self):
        res = self.manager.hold(channel_id=CHANNEL['id'])
        expect = [
            ('POST', '/channels/%s/hold' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_list(self):
        res = self.manager.list()
        expect = [
            ('GET', '/channels', {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(len(res), 1)

    def test_mute(self):
        res = self.manager.mute(channel_id=CHANNEL['id'], **MUTE_CHANNEL)
        expect = [
            ('POST', '/channels/%s/mute' % CHANNEL['id'], {}, MUTE_CHANNEL),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)

    def test_remove_music(self):
        res = self.manager.remove_music(channel_id=CHANNEL['id'])
        expect = [
            ('DELETE', '/channels/%s/moh' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_show(self):
        res = self.manager.get(channel_id=CHANNEL['id'])
        expect = [
            ('GET', '/channels/%s' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res.id, CHANNEL['id'])

    def test_unhold(self):
        res = self.manager.unhold(channel_id=CHANNEL['id'])
        expect = [
            ('DELETE', '/channels/%s/hold' % CHANNEL['id'], {}, None),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertEqual(res, None)

    def test_unmute(self):
        res = self.manager.unmute(channel_id=CHANNEL['id'], **MUTE_CHANNEL)
        expect = [
            ('POST', '/channels/%s/unmute' % CHANNEL['id'], {}, MUTE_CHANNEL),
        ]
        self.assertEqual(self.api.calls, expect)
        self.assertTrue(res)
