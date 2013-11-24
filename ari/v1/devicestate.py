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

UPDATE_ATTRIBUTES = [
    'deviceName',
    'deviceState',
]


class DeviceState(base.Resource):
    def __repr__(self):
        return '<Device State %s>' % self._info


class DeviceStateManager(base.Manager):

    resource_class = DeviceState

    @staticmethod
    def _path(id=None):
        return '/deviceStates/%s' % id if id else '/deviceStates'

    def update(self, device_state_id, **kwargs):
        keys = {}
        for (key, value) in kwargs.items():
            if key in UPDATE_ATTRIBUTES:
                keys[key] = value
            else:
                raise exception.InvalidAttribute()

        return self._update(self._path(device_state_id), keys)

    def delete(self, device_state_id):
        return self._delete(self._path(device_state_id))

    def get(self, device_state_id):
        try:
            return self._list(self._path(device_state_id))[0]
        except IndexError:
            return None

    def list(self):
        return self._list(self._path())
