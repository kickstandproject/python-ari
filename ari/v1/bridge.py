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

ADD_ATTRIBUTES = [
    'channel',
    'role',
]

CREATE_ATTRIBUTES = [
    'type',
]

MUSIC_ATTRIBUTES = [
    'mohClass',
]

REMOVE_ATTRIBUTES = [
    'channel',
]

PLAY_ATTRIBUTES = [
    'media',
    'lang',
    'offsetms',
    'skipms',
]


class Bridge(base.Resource):
    def __repr__(self):
        return '<Bridge %s>' % self._info


class BridgeManager(base.Manager):

    resource_class = Bridge

    def __create(self, attributes, path, callback, **kwargs):
        keys = {}
        for (key, value) in kwargs.items():
            if key in attributes:
                keys[key] = value
            else:
                raise exception.InvalidAttribute()

        return self._create(path, keys, callback=callback)

    @staticmethod
    def _path(uuid=None):
        return '/bridges/%s' % uuid if uuid else '/bridges'

    def add_audio(self, uuid, callback=None, **kwargs):
        path = '%s/%s' % (self._path(uuid), 'play')

        return self.__create(
            attributes=PLAY_ATTRIBUTES, path=path, callback=callback, **kwargs)

    def add(self, uuid, callback=None, **kwargs):
        path = '%s/%s' % (self._path(uuid), 'addChannel')

        return self.__create(
            attributes=ADD_ATTRIBUTES, path=path, callback=callback, **kwargs)

    def create(self, uuid=None, callback=None, **kwargs):
        path = self._path(uuid)

        return self.__create(
            attributes=CREATE_ATTRIBUTES, path=path, callback=callback,
            **kwargs)

    def delete(self, uuid, callback=None):
        return self._delete(self._path(uuid), callback=callback)

    def get(self, uuid, callback=None):
        try:
            return self._list(self._path(uuid), callback=callback)
        except IndexError:
            return None

    def add_music(self, uuid, callback=None, **kwargs):
        path = '%s/%s' % (self._path(uuid), 'moh')

        return self.__create(
            attributes=MUSIC_ATTRIBUTES, path=path, callback=callback,
            **kwargs)

    def list(self, callback=None):
        return self._list(self._path(), callback=callback)

    def remove(self, uuid, callback=None, **kwargs):
        path = '%s/%s' % (self._path(uuid), 'removeChannel')

        return self.__create(
            attributes=ADD_ATTRIBUTES, path=path, callback=callback, **kwargs)

    def remove_music(self, uuid, callback=None):
        path = '%s/%s' % (self._path(uuid), 'moh')

        return self._delete(path, callback=callback)
