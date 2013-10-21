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

import json
import pprint
import urlparse

from tornado.ioloop import IOLoop
from tornado.websocket import websocket_connect

from ari.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class Event(object):

    def __init__(self, url, username, password, app):
        self.app = app
        self.conn = None
        self.events = {}

        parts = urlparse.urlsplit(url)
        netloc = '%s:%s@%s:%s' % (
            username, password, parts.hostname, parts.port)
        path = '%s/%s' % (parts.path, 'events')
        query = 'app=%s' % app
        scheme = {
            'http': 'ws',
            'https': 'wss',
            'ws': 'ws',
            'wss': 'wss',
       }[parts.scheme]

        _url = urlparse.urlunsplit(
            (scheme, netloc, path, query, None))

        websocket_connect(_url, callback=self._on_connect)

    def _on_connect(self, ws):
        LOG.debug('Connected')
        self.conn = ws.result()
        self.conn.read_message(self._read_message)

    def _read_message(self, future):
        data = json.loads(future.result())

        if data['type'] in self.events:
            LOG.debug(
                'Received data from ARI event system: \n%s' %
                pprint.pformat(data))
            func = self.events[data['type']]
            IOLoop.instance().add_callback(func, data)

        self.conn.read_message(self._read_message)

    def register_event(self, name, callback):
        LOG.debug(
            "Registering callback '%s' for event '%s'" % (callback, name))
        self.events[name] = callback

    def unregister_event(self, name):
        LOG.debug(
            "Unregistering event '%s'" % name)
        del self.events[name]
