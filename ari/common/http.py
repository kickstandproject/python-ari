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

import logging

try:
    import json
except ImportError:
    import simplejson as json

from tornado import httpclient

LOG = logging.getLogger(__name__)


class HTTPClient(object):

    def __init__(self, username, password, endpoint):
        self.endpoint = endpoint
        self.password = password
        self.username = username
        self.client = httpclient.AsyncHTTPClient()

    def json_request(self, url, callback=None, **kwargs):
        if 'body' in kwargs:
            kwargs['body'] = json.dumps(kwargs['body'])
        headers = {
            'Content-Type': 'application/json'
        }
        url = self.endpoint + url
        self.client.fetch(
            url, callback, headers=headers, auth_username=self.username,
            auth_password=self.password, **kwargs)
