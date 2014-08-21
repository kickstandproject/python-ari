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

    def __create(self, attributes, path, callback, **kwargs):
        keys = {}
        for (key, value) in kwargs.items():
            if key in attributes:
                keys[key] = value
            else:
                message = key
                raise exception.InvalidAttribute(message=message)

        return self._create(path, keys, callback=callback)

    @staticmethod
    def _path(uuid=None):
        return '/channels/%s' % uuid if uuid else '/channels'

    def add_audio(self, uuid, callback=None, **kwargs):
        path = '%s/%s' % (self._path(uuid), 'play')

        return self.__create(
            attributes=PLAY_ATTRIBUTES, path=path, callback=callback, **kwargs)

    def add_music(self, uuid, callback=None, **kwargs):
        """Add music to the given channel.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'moh')

        return self.__create(
            attributes=MUSIC_ATTRIBUTES, path=path, callback=callback,
            **kwargs)

    def answer(self, uuid, callback=None):
        """Answer the given channel.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'answer')

        return self.__create(
            attributes=None, path=path, callback=callback)

    def create(self, uuid=None, callback=None, **kwargs):
        """Create a new channel."

        :param uuid: Unique identifier of the channel.
        """

        path = self._path(uuid)

        return self.__create(
            attributes=CREATE_ATTRIBUTES, path=path, callback=callback,
            **kwargs)

    def delete(self, uuid, callback=None):
        """Hangup the given channel.

        :param uuid: ID of the channel within the stasis application.
        """

        return self._delete(self._path(uuid), callback=None)

    def dial(self, uuid, callback=None, **kwargs):
        path = '%s/%s' % (self._path(uuid), 'dial')

        return self.__create(
            attributes=DIAL_ATTRIBUTES, path=path, callback=callback, **kwargs)

    def exit(self, uuid, callback=None, **kwargs):
        """Exit the given channel from stasis.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'continue')

        return self.__create(
            attributes=EXIT_ATTRIBUTES, path=path, callback=callback, **kwargs)

    def get(self, uuid, callback=None):
        """Get information of the given channel.

        :param uuid: ID of the channel within the stasis application.
        """

        try:
            return self._list(self._path(uuid), callback=callback)[0]
        except IndexError:
            return None

    def hold(self, uuid, callback=None):
        """Place the given channel on hold.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'hold')

        return self.__create(
            attributes=None, path=path, callback=callback)

    def list(self, callback=None):
        """List active channels."""

        return self._list(self._path(), callback=callback)

    def mute(self, uuid, callback=None, **kwargs):
        """Mute the given channel.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'mute')

        return self.__create(
            attributes=MUTE_ATTRIBUTES, path=path, callback=callback, **kwargs)

    def remove_music(self, uuid, callback=None):
        """Remove music from the given channel.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'moh')

        return self._delete(path, callback=callback)

    def unhold(self, uuid, callback=None):
        """Remove the given channel from hold.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'hold')

        return self._delete(path, callback=callback)

    def unmute(self, uuid, callback=None, **kwargs):
        """Remove the given channel from mute.

        :param uuid: ID of the channel within the stasis application.
        """

        path = '%s/%s' % (self._path(uuid), 'unmute')

        return self.__create(
            attributes=MUTE_ATTRIBUTES, path=path, callback=callback, **kwargs)
