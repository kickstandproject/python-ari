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


class Channel(base.Resource):
    def __repr__(self):
        return '<Channel %s>' % self._info


class ChannelManager(base.Manager):

    resource_class = Channel

    @staticmethod
    def _path(id=None):
        return '/channels/%s' % id if id else '/channels'

    def delete(self, channel_id):
        return self._delete(self._path(channel_id))

    def get(self, channel_id):
        try:
            return self._list(self._path(channel_id))[0]
        except IndexError:
            return None

    def list(self):
        return self._list(self._path())
