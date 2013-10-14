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


class ListApplication(base.ListCommand):
    """List applications."""

    list_columns = [
        'name',
        'bridge_ids',
        'channel_ids',
        'endpoint_ids',
    ]
    log = logging.getLogger(__name__ + '.ListApplication')
    resource = 'applications'


class ShowApplication(base.ShowCommand):
    """Show information of a given application."""

    log = logging.getLogger(__name__ + '.ShowApplication')
    resource = 'applications'
