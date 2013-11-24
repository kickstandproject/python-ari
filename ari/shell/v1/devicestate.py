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


class CreateDeviceState(base.UpdateCommand):
    """Create a Device State."""

    log = logging.getLogger(__name__ + '.CreateDeviceState')
    resource = 'devicestates'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'state', metavar='STATE', help='Device state value.')

    def args2body(self, parsed_args):
        body = {
            'deviceState': parsed_args.state,
        }

        return body


class DeleteDeviceState(base.DeleteCommand):
    """Delete a given Device State."""

    log = logging.getLogger(__name__ + '.DeleteDeviceState')
    resource = 'devicestates'


class ListDeviceState(base.ListCommand):
    """List Device States."""

    list_columns = [
        'name',
        'state',
    ]
    log = logging.getLogger(__name__ + '.ListDeviceState')
    resource = 'devicestates'


class ShowDeviceState(base.ShowCommand):
    """Show information of a given device state."""

    log = logging.getLogger(__name__ + '.ShowDeviceState')
    resource = 'devicestates'
