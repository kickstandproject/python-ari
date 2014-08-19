# -*- coding: utf-8 -*-
# Copyright 2012 OpenStack LLC.
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

from ari.common import http
from ari.v1 import bridge
from ari.v1 import channel


class Client(http.HTTPClient):
    """Client for the ARI v1 API."""

    def __init__(self, *args):
        super(Client, self).__init__(*args)
        self.bridges = bridge.BridgeManager(self)
        self.channels = channel.ChannelManager(self)
