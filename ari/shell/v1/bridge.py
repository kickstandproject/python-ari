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

import logging

from ari.shell.v1 import base


class ListBridge(base.ListCommand):

    list_columns = [
        'id',
        'technology',
        'bridge_type',
        'bridge_class',
        'channels',
    ]
    log = logging.getLogger(__name__ + '.ListBridge')
    resource = 'bridges'