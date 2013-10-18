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

    def __create(self, attributes, path, **kwargs):
        keys = {}
        for (key, value) in kwargs.items():
            if key in attributes:
                keys[key] = value
            else:
                raise exception.InvalidAttribute()

        return self._create(path, keys)

    @staticmethod
    def _path(id=None):
        return '/bridges/%s' % id if id else '/bridges'

    def add_audio(self, bridge_id, **kwargs):
        path = '%s/%s' % (self._path(bridge_id), 'play')

        return self.__create(
            attributes=PLAY_ATTRIBUTES, path=path, **kwargs)

    def add(self, bridge_id, **kwargs):
        path = '%s/%s' % (self._path(bridge_id), 'addChannel')

        return self.__create(
            attributes=ADD_ATTRIBUTES, path=path, **kwargs)

    def create(self, **kwargs):
        path = self._path()

        return self.__create(
            attributes=CREATE_ATTRIBUTES, path=path, **kwargs)

    def delete(self, bridge_id):
        return self._delete(self._path(bridge_id))

    def get(self, bridge_id):
        try:
            return self._list(self._path(bridge_id))[0]
        except IndexError:
            return None

    def add_music(self, bridge_id, **kwargs):
        path = '%s/%s' % (self._path(bridge_id), 'moh')

        return self.__create(
            attributes=MUSIC_ATTRIBUTES, path=path, **kwargs)

    def list(self):
        return self._list(self._path())

    def remove(self, bridge_id, **kwargs):
        path = '%s/%s' % (self._path(bridge_id), 'removeChannel')

        return self.__create(
            attributes=ADD_ATTRIBUTES, path=path, **kwargs)

    def remove_music(self, bridge_id):
        path = '%s/%s' % (self._path(bridge_id), 'moh')

        return self._delete(path)
