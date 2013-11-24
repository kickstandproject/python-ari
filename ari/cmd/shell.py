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

"""
Command-line interface to the ARI APIs.
"""

import sys

from cliff import app
from cliff import commandmanager
from oslo.config import cfg

from ari import client
from ari.common import utils
from ari import exception
from ari.openstack.common import log as logging
from ari.shell.v1 import application
from ari.shell.v1 import bridge
from ari.shell.v1 import channel
from ari.shell.v1 import devicestate
from ari.shell.v1 import endpoint
from ari.shell.v1 import sound

CONF = cfg.CONF

COMMAND = {
    'application-list': application.ListApplication,
    'application-show': application.ShowApplication,
    'bridge-audio-add': bridge.AddAudioBridge,
    'bridge-channel-add': bridge.AddChannelBridge,
    'bridge-channel-remove': bridge.RemoveChannelBridge,
    'bridge-create': bridge.CreateBridge,
    'bridge-delete': bridge.DeleteBridge,
    'bridge-list': bridge.ListBridge,
    'bridge-music-add': bridge.AddMusicBridge,
    'bridge-music-remove': bridge.RemoveMusicBridge,
    'bridge-show': bridge.ShowBridge,
    'channel-answer': channel.AnswerChannel,
    'channel-audio-add': channel.AddAudioChannel,
    'channel-exit': channel.ExitChannel,
    'channel-create': channel.CreateChannel,
    'channel-delete': channel.DeleteChannel,
    'channel-dial': channel.DialChannel,
    'channel-hold-add': channel.AddHoldChannel,
    'channel-hold-remove': channel.RemoveHoldChannel,
    'channel-list': channel.ListChannel,
    'channel-music-add': channel.AddMusicChannel,
    'channel-music-remove': channel.RemoveMusicChannel,
    'channel-mute-add': channel.AddMuteChannel,
    'channel-mute-remove': channel.RemoveMuteChannel,
    'channel-show': channel.ShowChannel,
    'device-state-create': devicestate.CreateDeviceState,
    'device-state-delete': devicestate.DeleteDeviceState,
    'device-state-list': devicestate.ListDeviceState,
    'device-state-show': devicestate.ShowDeviceState,
    'endpoint-list': endpoint.ListEndpoint,
    'endpoint-show': endpoint.ShowEndpoint,
    'sound-list': sound.ListSound,
    'sound-show': sound.ShowSound,
}

COMMANDS = {
    '1': COMMAND
}

LOG = logging.getLogger(__name__)

VERSION = '1'


class Shell(app.App):

    def __init__(self, apiversion='1'):
        super(Shell, self).__init__(
            description=__doc__.strip(),
            version=VERSION,
            command_manager=commandmanager.CommandManager('ari.cli'),
        )
        self.commands = COMMANDS
        for k, v in self.commands[apiversion].items():
            self.command_manager.add_command(k, v)

        self.api_version = apiversion

    def authenticate_user(self):
        if not self.options.ari_username:
            raise exception.CommandError(
                'You must provide a username via either --ari-username or'
                ' env[ARI_USERNAME]'
            )

        if not self.options.ari_password:
            raise exception.CommandError(
                'You must provide a password via either --ari-password or'
                ' env[ARI_PASSWORD]'
            )

        if not self.options.ari_url:
            raise exception.CommandError(
                'You must provide an url via either --ari-url or env[ARI_URL]'
            )

        self.client_manager = client.get_client(
            self.api_version, **(self.options.__dict__)
        )

        return

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super(Shell, self).build_option_parser(
            description, version, argparse_kwargs
        )

        parser.add_argument(
            '--ari-url',
            default=utils.env('ARI_URL'),
            help='Defaults to env[ARI_URL]')
        parser.add_argument(
            '--ari-username',
            default=utils.env('ARI_USERNAME'),
            help='Defaults to env[ARI_USERNAME]')
        parser.add_argument(
            '--ari-password',
            default=utils.env('ARI_PASSWORD'),
            help='Defaults to env[ARI_PASSWORD]')
        parser.add_argument(
            '--ca-file', help='Path of CA SSL certificate(s) used to verify '
            'the remote server certificate. Without this option we look for '
            'the default system CA certificates')
        parser.add_argument(
            '--cert-file', help='Path of certificate file to use in SSL '
            'connection')
        parser.add_argument(
            '-k', '--insecure', default=False, action='store_true',
            help="Explicitly allow \"insecure\" SSL (https) requests. The "
            "server's certificate will not be verified against any "
            "certificate authorities. This options should be used with "
            "caution")

        return parser

    def configure_logging(self):
        if self.options.debug:
            CONF.debug = True
        elif self.options.verbose_level:
            CONF.verbose = True

        return

    def initialize_app(self, argv):
        super(Shell, self).initialize_app(argv)

        logging.setup('ari')
        cmd_name = None

        if argv:
            cmd_info = self.command_manager.find_command(argv)
            cmd_factory, cmd_name, sub_argv = cmd_info

        if self.interactive_mode or cmd_name != 'help':
            self.authenticate_user()


def main(argv=sys.argv[1:]):
    return Shell().run(argv)
