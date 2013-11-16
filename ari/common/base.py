# -*- coding: utf-8 -*-
# Copyright 2012 OpenStack LLC.
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

import copy


class Manager(object):

    resource_class = None

    def __init__(self, api):
        self.api = api

    def _create(self, url, body):
        resp, body = self.api.json_request('POST', url, body=body)
        if body:
            return self.resource_class(self, body)

    def _delete(self, url):
        self.api.raw_request('DELETE', url)

    def _list(self, url, response_key=None, obj_class=None, body=None):
        resp, body = self.api.json_request('GET', url)

        if obj_class is None:
            obj_class = self.resource_class

        if response_key:
            try:
                data = body[response_key]
            except KeyError:
                return []
        else:
            data = body

        if not isinstance(data, list):
            data = [data]

        return [obj_class(self, res, loaded=True) for res in data if res]

    def _update(self, url, body, response_key=None):
        resp, body = self.api.json_request('PUT', url, body=body)
        # PUT requests may not return a body
        if body:
            return self.resource_class(self, body)


class Resource(object):

    def __init__(self, manager, info, loaded=False):
        self.manager = manager
        self._info = info
        self._add_details(info)
        self._loaded = loaded

    def _add_details(self, info):
        for (k, v) in info.iteritems():
            setattr(self, k, v)

    def __getattr__(self, k):
        if k not in self.__dict__:
            if not self.is_loaded():
                self.get()

                return self.__getattr__(k)

            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys() if k[0] != '_' and
                          k != 'manager')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)

        return "<%s %s>" % (self.__class__.__name__, info)

    def get(self):
        self.set_loaded(True)
        if not hasattr(self.manager, 'get'):
            return

        new = self.manager.get(self.id)
        if new:
            self._add_details(new._info)

    def is_loaded(self):
        return self._loaded

    def to_dict(self):
        return copy.deepcopy(self._info)
