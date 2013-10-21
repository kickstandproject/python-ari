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

from oslo.config import cfg
from tornado.ioloop import IOLoop

from ari import client
from ari.common import utils
from ari import event
from ari.openstack.common import log as logging

CONF = cfg.CONF


ARI_OPTIONS = {
    'ari_url': utils.env('ARI_URL'),
    'ari_username': utils.env('ARI_USERNAME'),
    'ari_password': utils.env('ARI_PASSWORD'),
}

STASIS_OPTIONS = {
    'url': utils.env('ARI_URL'),
    'username': utils.env('ARI_USERNAME'),
    'password': utils.env('ARI_PASSWORD'),
    'app': 'demo',
}


class Demo(object):
    log = logging.getLogger('Demo')

    def __init__(self):
        self._client = client.get_client('1', **ARI_OPTIONS)
        self._events = event.Event(**STASIS_OPTIONS)
        self._events.register_event('StasisStart', self.handle_stasis_start)
        self._events.register_event('StasisEnd', self.handle_stasis_end)

    def handle_channel_state_change(self, data):
        channel = data['channel']['id']
        self._events.unregister_event('ChannelStateChange')
        self.log.info("Placing channel '%s' on hold" % channel)
        self._client.channels.add_music(channel)

    def handle_stasis_end(self, data):
        channel = data['channel']['id']
        self.log.info("Channel '%s' disconnected" % channel)

    def handle_stasis_start(self, data):
        self.log.info('Incoming call')
        channel = data['channel']['id']
        self._events.register_event(
            'ChannelStateChange', self.handle_channel_state_change)
        self._client.channels.answer(channel)


def main():
    CONF.verbose = True
    logging.setup('demo')

    Demo()
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
