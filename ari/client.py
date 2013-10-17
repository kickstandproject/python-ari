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


def get_client(api_version, **kwargs):
    endpoint = kwargs.get('ari_url')
    password = kwargs.get('ari_password', None)
    token = None
    username = kwargs.get('ari_username', None)

    if (password and username):
        auth = base64.encodestring(
            '%s:%s' % (username, password)
        ).replace('\n', '')
        token = 'Basic %s' % auth

    cli_kwargs = {
        'ca_file': kwargs.get('ca_file'),
        'cert_file': kwargs.get('cert_file'),
        'insecure': kwargs.get('insecure'),
        'key_file': kwargs.get('key_file'),
        'token': token
    }

    return Client(api_version, endpoint, **cli_kwargs)


def Client(version, *args, **kwargs):
    module = utils.import_versioned_module(version, 'client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)
