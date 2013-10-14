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

DIAL_ATTRIBUTES = [
    'context',
    'endpoint',
    'extension',
    'timeout',
]

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


class Channel(base.Resource):
    def __repr__(self):
        return '<Channel %s>' % self._info


class ChannelManager(base.Manager):

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

    def answer(self, channel_id):
        path = '%s/%s' % (self._path(channel_id), 'answer')

        return self._create(path, None)

    def create(self, **kwargs):
        path = self._path()
        return self.__create(
            attributes=CREATE_ATTRIBUTES, path=path, **kwargs)

    def delete(self, channel_id):
        return self._delete(self._path(channel_id))

    def dial(self, channel_id, **kwargs):
        path = '%s/%s' % (self._path(channel_id), 'dial')

        return self.__create(
            attributes=DIAL_ATTRIBUTES, path=path, **kwargs)

    def get(self, channel_id):
        try:
            return self._list(self._path(channel_id))[0]
        except IndexError:
            return None

    def list(self):
        return self._list(self._path())
