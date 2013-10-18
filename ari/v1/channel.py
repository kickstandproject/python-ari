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

from ari.common import base
from ari import exception

CREATE_ATTRIBUTES = [
    'app',
    'appArgs',
    'callerId',
    'context',
    'endpoint',
    'extension',
    'priority',
    'timeout',
]

DIAL_ATTRIBUTES = [
    'context',
    'endpoint',
    'extension',
    'timeout',
]

EXIT_ATTRIBUTES = [
    'context',
    'extension',
    'priority',
]

MUSIC_ATTRIBUTES = [
    'mohClass',
]

MUTE_ATTRIBUTES = [
    'direction',
]

PLAY_ATTRIBUTES = [
    'media',
    'lang',
    'offsetms',
    'skipms',
]


class Channel(base.Resource):
    def __repr__(self):
        return '<Channel %s>' % self._info


class ChannelManager(base.Manager):
    """Channel resource."""

    resource_class = Channel

    def __create(self, attributes, path, **kwargs):
        keys = {}
        for (key, value) in kwargs.items():
            if key in attributes:
                keys[key] = value
            else:
                message = key
                raise exception.InvalidAttribute(message=message)

        return self._create(path, keys)

    @staticmethod
    def _path(id=None):
        return '/channels/%s' % id if id else '/channels'

    def add_audio(self, channel_id, **kwargs):
        path = '%s/%s' % (self._path(channel_id), 'play')

        return self.__create(
            attributes=PLAY_ATTRIBUTES, path=path, **kwargs)

    def add_music(self, channel_id, **kwargs):
        """Add music to the given channel.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'moh')

        return self.__create(
            attributes=MUSIC_ATTRIBUTES, path=path, **kwargs)

    def answer(self, channel_id):
        """Answer the given channel.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'answer')

        return self._create(path, None)

    def create(self, **kwargs):
        path = self._path()

        return self.__create(
            attributes=CREATE_ATTRIBUTES, path=path, **kwargs)

    def delete(self, channel_id):
        """Hangup the given channel.

        :param channel_id: ID of the channel within the stasis application.
        """

        return self._delete(self._path(channel_id))

    def dial(self, channel_id, **kwargs):
        path = '%s/%s' % (self._path(channel_id), 'dial')

        return self.__create(
            attributes=DIAL_ATTRIBUTES, path=path, **kwargs)

    def exit(self, channel_id, **kwargs):
        """Exit the given channel from stasis.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'continue')

        return self.__create(
            attributes=EXIT_ATTRIBUTES, path=path, **kwargs)

    def get(self, channel_id):
        """Get information of the given channel.

        :param channel_id: ID of the channel within the stasis application.
        """

        try:
            return self._list(self._path(channel_id))[0]
        except IndexError:
            return None

    def hold(self, channel_id):
        """Place the given channel on hold.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'hold')

        return self._create(path, None)

    def list(self):
        """List active channels."""

        return self._list(self._path())

    def mute(self, channel_id, **kwargs):
        """Mute the given channel.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'mute')

        return self.__create(
            attributes=MUTE_ATTRIBUTES, path=path, **kwargs)

    def remove_music(self, channel_id):
        """Remove music from the given channel.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'moh')

        return self._delete(path)

    def unhold(self, channel_id):
        """Remove the given channel from hold.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'hold')

        return self._delete(path)

    def unmute(self, channel_id, **kwargs):
        """Remove the given channel from mute.

        :param channel_id: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(channel_id), 'unmute')

        return self.__create(
            attributes=MUTE_ATTRIBUTES, path=path, **kwargs)
