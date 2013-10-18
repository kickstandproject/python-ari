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


class AddAudioBridge(base.CreateCommand):
    """Add audio to a given bridge."""

    function = 'add_audio'
    resource = 'bridges'
    log = logging.getLogger(__name__ + '.AddAudioBridge')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--offset', help='How long to skip (in milliseconds) before '
            'playing the audio.')
        parser.add_argument(
            '--skip', help='Number of milliseconds to skip forward and '
            'reverse while using the Playback resource.')
        parser.add_argument(
            'bridge_id', metavar='BRIDGE', help='Bridge id to use.')
        parser.add_argument(
            'uri', metavar='URI', help='Media URI to use.')

    def args2body(self, parsed_args):
        body = {
            'bridge_id': parsed_args.bridge_id,
            'media': parsed_args.uri,
        }

        if parsed_args.offset:
            body['offsetms'] = parsed_args.offset
        if parsed_args.skip:
            body['skipms'] = parsed_args.skip

        return body


class AddChannelBridge(base.CreateCommand):
    """Add a given channel to bridge."""

    function = 'add'
    resource = 'bridges'
    log = logging.getLogger(__name__ + '.AddChannelBridge')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--role', help='Channels role in the bridge.')
        parser.add_argument(
            'bridge_id', metavar='BRIDGE', help='Bridge id to use.')
        parser.add_argument(
            'channel_id', metavar='CHANNEL', help='Channel id to use.')

    def args2body(self, parsed_args):
        body = {
            'bridge_id': parsed_args.bridge_id,
            'channel': parsed_args.channel_id,
        }

        if parsed_args.role:
            body['role'] = parsed_args.role

        return body


class AddMusicBridge(base.CreateCommand):
    """Add music to a given bridge."""

    function = 'add_music'
    resource = 'bridges'
    log = logging.getLogger(__name__ + '.AddMusicBridge')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--moh_class', help='Which class to use.')
        parser.add_argument(
            'bridge_id', metavar='BRIDGE', help='Bridge id to use.')

    def args2body(self, parsed_args):
        body = {
            'bridge_id': parsed_args.bridge_id,
        }

        if parsed_args.moh_class:
            body['mohClass'] = parsed_args.moh_class

        return body


class CreateBridge(base.CreateCommand):
    """Create a bridge."""

    log = logging.getLogger(__name__ + '.CreateBridge')
    resource = 'bridges'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--bridge_type', default='mixing', help='Type of bridge to'
            ' create.')

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


class RemoveChannelBridge(base.CreateCommand):
    """Remove a given channel from bridge."""

    function = 'remove'
    resource = 'bridges'
    log = logging.getLogger(__name__ + '.RemoveChannelBridge')

    def add_known_arguments(self, parser):
        parser.add_argument(
            'bridge_id', metavar='BRIDGE', help='Bridge id to use.')
        parser.add_argument(
            'channel_id', metavar='CHANNEL', help='Channel id to use.')

    def args2body(self, parsed_args):
        body = {
            'bridge_id': parsed_args.bridge_id,
            'channel': parsed_args.channel_id,
        }

        return body


class ShowBridge(base.ShowCommand):
    """Show information of a given bridge."""

    log = logging.getLogger(__name__ + '.ShowBridge')
    resource = 'bridges'


class RemoveMusicBridge(base.ShowCommand):
    """Remove music from a given bridge."""

    function = 'remove_music'
    resource = 'bridges'
    log = logging.getLogger(__name__ + '.RemoveMusicBridge')
