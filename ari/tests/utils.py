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

    # Note(pabelanger): Work around upstream bug[1] and this function should be
    # deleted once we can POST json directly to ARI.
    #
    # [1] https://issues.asterisk.org/jira/browse/ASTERISK-22685
    #
    def url_encode_request(self, *args, **kwargs):
        return self.json_request(*args, **kwargs)


class FakeResponse(object):

    def __init__(self, headers, body=None, version=None):
        self.headers = headers
        self.body = body
