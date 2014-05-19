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

import base64

from ari.common import utils


def get_client(api_version, username, password, endpoint):
    auth = base64.encodestring(
        '%s:%s' % (username, password)
    ).replace('\n', '')
    token = 'Basic %s' % auth

    return Client(api_version, endpoint, token)


def Client(version, *args):
    module = utils.import_versioned_module(version, 'client')
    client_class = getattr(module, 'Client')
    return client_class(*args)
