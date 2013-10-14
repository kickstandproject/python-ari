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


class CreateBridge(base.CreateCommand):
    """Create a bridge."""

    log = logging.getLogger(__name__ + '.CreateBridge')
    resource = 'bridges'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'bridge_type', metavar='BRIDGE_TYPE',
            help='Type of bridge to create.')

    def args2body(self, parsed_args):
        body = {
            'type': parsed_args.bridge_type,
        }

        return body


class DeleteBridge(base.DeleteCommand):
    """Delete a given bridge."""

    log = logging.getLogger(__name__ + '.DeleteBridge')
    resource = 'bridges'


class ListBridge(base.ListCommand):
    """List bridges."""

    list_columns = [
        'id',
        'technology',
        'bridge_type',
        'bridge_class',
        'channels',
    ]
    log = logging.getLogger(__name__ + '.ListBridge')
    resource = 'bridges'


class ShowBridge(base.ShowCommand):
    """Show information of a given bridge."""

    log = logging.getLogger(__name__ + '.ShowBridge')
    resource = 'bridges'
