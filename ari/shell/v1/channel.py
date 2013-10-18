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


class AddAudioChannel(base.CreateCommand):
    """Add audio to a given channel."""

    function = 'add_audio'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.AddAudioChannel')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--offset', help='How long to skip (in milliseconds) before '
            'playing the audio.')
        parser.add_argument(
            '--skip', help='Number of milliseconds to skip forward and '
            'reverse while using the Playback resource.')
        parser.add_argument(
            'channel_id', metavar='CHANNEL', help='Channel id to use.')
        parser.add_argument(
            'uri', metavar='URI', help='Media URI to use.')

    def args2body(self, parsed_args):
        body = {
            'channel_id': parsed_args.channel_id,
            'media': parsed_args.uri,
        }

        if parsed_args.offset:
            body['offsetms'] = parsed_args.offset
        if parsed_args.skip:
            body['skipms'] = parsed_args.skip

        return body


class AddMusicChannel(base.CreateCommand):
    """Add music to a given channel."""

    function = 'add_music'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.AddMusicChannel')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--moh_class', help='Which class to use.')
        parser.add_argument(
            'channel_id', metavar='CHANNEL', help='Channel id to use.')

    def args2body(self, parsed_args):
        body = {
            'channel_id': parsed_args.channel_id,
        }

        if parsed_args.moh_class:
            body['mohClass'] = parsed_args.moh_class

        return body


class AnswerChannel(base.ShowCommand):
    """Answer a given channel."""

    function = 'answer'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.AnswerChannel')


class AddHoldChannel(base.ShowCommand):
    """Add a given channel to hold."""

    function = 'hold'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.AddHoldChannel')


class AddMuteChannel(base.CreateCommand):
    """Add a given channel to mute."""

    function = 'mute'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.AddMuteChannel')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--direction', default='both',
            help='Direction in which to mute the audio.')
        parser.add_argument(
            'channel_id', metavar='CHANNEL', help='Channel id to use.')

    def args2body(self, parsed_args):
        body = {
            'channel_id': parsed_args.channel_id,
            'direction': parsed_args.direction,
        }

        return body


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


class DialChannel(base.CreateCommand):
    """Dial a given channel."""

    function = 'dial'
    log = logging.getLogger(__name__ + '.DialChannel')
    resource = 'channels'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--context', help='The context to dial after the endpoint'
            ' answers. (Default: demo)')
        parser.add_argument(
            '--endpoint', help='Endpoint to call.')
        parser.add_argument(
            '--extension', help='The extension to dial after the endpoint'
            ' answers.')
        parser.add_argument(
            '--timeout', help='The timeout (in seconds) before giving up'
            ' dialing.')
        parser.add_argument(
            'channel_id', metavar='CHANNEL', help='Channel id to use.')

    def args2body(self, parsed_args):
        body = {
            'channel_id': parsed_args.channel_id
        }
        if parsed_args.context:
            body['context'] = parsed_args.context
        if parsed_args.endpoint:
            body['endpoint'] = parsed_args.endpoint
        if parsed_args.extension:
            body['extension'] = parsed_args.extension
        if parsed_args.timeout:
            body['timeout'] = parsed_args.timeout

        return body


class ExitChannel(base.CreateCommand):
    """Exit a given channel."""

    function = 'exit'
    log = logging.getLogger(__name__ + '.DialChannel')
    resource = 'channels'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--context', help='The context to use.')
        parser.add_argument(
            '--extension', help='The extension to use.')
        parser.add_argument(
            '--priority', help='The priority to use.')
        parser.add_argument(
            'channel_id', metavar='CHANNEL', help='Channel id to use.')

    def args2body(self, parsed_args):
        body = {
            'channel_id': parsed_args.channel_id
        }
        if parsed_args.context:
            body['context'] = parsed_args.context
        if parsed_args.extension:
            body['extension'] = parsed_args.extension
        if parsed_args.priority:
            body['priority'] = parsed_args.timeout

        return body


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


class RemoveHoldChannel(base.ShowCommand):
    """Remove a given channel from hold."""

    function = 'unhold'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.RemoveHoldChannel')


class RemoveMusicChannel(base.ShowCommand):
    """Remove music from a given channel."""

    function = 'remove_music'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.RemoveMusicChannel')


class RemoveMuteChannel(AddMuteChannel):
    """Remove a given channel to mute."""

    function = 'unmute'
    resource = 'channels'
    log = logging.getLogger(__name__ + '.RemoveMuteChannel')


class ShowChannel(base.ShowCommand):
    """Show information of a given channel."""

    resource = 'channels'
    log = logging.getLogger(__name__ + '.ShowChannel')
