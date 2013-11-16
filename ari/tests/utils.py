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

import StringIO

from ari.common import http


class FakeAPI(object):

    def __init__(self, fixtures):
        self.fixtures = fixtures
        self.calls = []

    def _request(self, method, url, headers=None, body=None):
        call = (method, url, headers or {}, body)
        self.calls.append(call)

        return self.fixtures[url][method]

    def json_request(self, *args, **kwargs):
        fixture = self._request(*args, **kwargs)

        return FakeResponse(fixture[0]), fixture[1]

    def raw_request(self, *args, **kwargs):
        fixture = self._request(*args, **kwargs)
        body_iter = http.ResponseBodyIterator(StringIO.StringIO(fixture[1]))

        return FakeResponse(fixture[0]), body_iter


class FakeResponse(object):

    def __init__(self, headers, body=None, version=None):
        self.headers = headers
        self.body = body
