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


class CreateChannel(base.CreateCommand):
    """Create a channel."""

    log = logging.getLogger(__name__ + '.CreateChannel')
    resource = 'channels'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--app', help='The application name to pass to the Statis'
            ' application.')
        parser.add_argument(
            '--appArgs', help='The application arguments to pass to the'
            ' Stasis application.')
        parser.add_argument(
            '--callerId', help='The CallerID to use when dialing and endpoint'
            ' or extension.')
        parser.add_argument(
            '--context', help='The context to dial after the endpoint'
            ' answers. (Default: demo)')
        parser.add_argument(
            '--extension', help='The extension to dial after the endpoint'
            ' answers.')
        parser.add_argument(
            '--priority', help='The priority to dial after the endpoint'
            ' answers. (Default: 1)')
        parser.add_argument(
            '--timeout', help='The timeout (in seconds) before giving up'
            ' dialing.')
        parser.add_argument(
            'endpoint', metavar='ENDPOINT', help='Endpoint to call.')

    def args2body(self, parsed_args):
        body = {
            'endpoint': parsed_args.endpoint,
        }
        if parsed_args.app:
            body['app'] = parsed_args.app
        if parsed_args.appArgs:
            body['appArgs'] = parsed_args.appArgs
        if parsed_args.callerId:
            body['callerId'] = parsed_args.callerId
        if parsed_args.context:
            body['context'] = parsed_args.context
        if parsed_args.extension:
            body['extension'] = parsed_args.extension
        if parsed_args.priority:
            body['priority'] = parsed_args.priority
        if parsed_args.timeout:
            body['timeout'] = parsed_args.timeout

        return body


class DeleteChannel(base.DeleteCommand):
    """Delete a given channel."""

    log = logging.getLogger(__name__ + '.DeleteChannel')
    resource = 'channels'


class ListChannel(base.ListCommand):
    """List channels."""

    list_columns = [
        'id',
        'name',
        'state',
        'caller',
        'connected',
        'accountcode',
        'dialplan',
        'creationtime',
    ]
    log = logging.getLogger(__name__ + '.ListChannel')
    resource = 'channels'


class ShowChannel(base.ShowCommand):
    """Show information of a given channel."""

    resource = 'channels'
    log = logging.getLogger(__name__ + '.ShowChannel')
