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
import httplib
import logging
import socket
import StringIO
import urlparse

try:
    import json
except ImportError:
    import simplejson as json

from ari import exception

LOG = logging.getLogger(__name__)
USER_AGENT = 'python-ari'
CHUNKSIZE = 1024 * 64  # 64kB


class HTTPClient(object):

    def __init__(self, endpoint, **kwargs):
        self.endpoint = endpoint
        self.auth_token = kwargs.get('token')
        self.connection_params = self.get_connection_params(endpoint, **kwargs)

    def _extract_error_message(self, body):
        try:
            body_json = json.loads(body)

            if 'message' in body_json:
                return body_json['message']

        except ValueError:
            pass

    def _http_request(self, url, method, **kwargs):
        kwargs['headers'] = copy.deepcopy(kwargs.get('headers', {}))
        kwargs['headers'].setdefault('User-Agent', USER_AGENT)
        if self.auth_token:
            kwargs['headers'].setdefault('Authorization', self.auth_token)

        self.log_curl_request(method, url, kwargs)
        conn = self.get_connection()

        try:
            conn_url = self._make_connection_url(url)
            conn.request(method, conn_url, **kwargs)
            resp = conn.getresponse()
        except socket.gaierror as e:
            message = (
                "Error finding address for %(url)s: %(e)s"
                % dict(url=url, e=e)
            )
            raise exception.InvalidEndpoint(message=message)
        except (socket.error, socket.timeout) as e:
            endpoint = self.endpoint
            message = (
                "Error communicating with %(endpoint)s %(e)s"
                % dict(endpoint=endpoint, e=e)
            )
            raise exception.CommunicationError(message=message)

        body_iter = ResponseBodyIterator(resp)
        body_str = None

        if resp.getheader('content-type', None) != 'application/octet-stream':
            body_str = ''.join([chunk for chunk in body_iter])
            self.log_http_response(resp, body_str)
            body_iter = StringIO.StringIO(body_str)
        else:
            self.log_http_response(resp)

        if 400 <= resp.status < 600:
            LOG.warn('Request returned failure status.')
            err_msg = self._extract_error_message(body_str)
            raise exception.from_response(resp, err_msg)
        elif resp.status in (301, 302, 305):
            return self._http_request(resp['location'], method, **kwargs)
        elif resp.status == 300:
            raise exception.from_resoinse(resp)

        return resp, body_iter

    def _make_connection_url(self, url):
        (_class, _args, _kwargs) = self.connection_params
        base_url = _args[2]

        return '%s/%s' % (base_url.rstrip('/'), url.lstrip('/'))

    @staticmethod
    def get_connection_params(endpoint, **kwargs):
        parts = urlparse.urlparse(endpoint)

        _args = (parts.hostname, parts.port, parts.path)
        _kwargs = {
            'timeout': (float(kwargs.get('timeout'))
                        if kwargs.get('timeout') else 600)
        }

        if parts.scheme == 'http':
            _class = httplib.HTTPConnection
        else:
            msg = 'Unsupported scheme: %s' % parts.scheme
            raise exception.InvalidEndpoint(msg)

        return (_class, _args, _kwargs)

    def get_connection(self):
        _class = self.connection_params[0]
        try:
            return _class(
                *self.connection_params[1][0:2],
                **self.connection_params[2]
            )
        except httplib.InvalidURL:
            raise exception.InvalidEndpoint()

    def json_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers'].setdefault('Accept', 'application/json')

        if 'body' in kwargs:
            kwargs['body'] = json.dumps(kwargs['body'])

        resp, body_iter = self._http_request(url, method, **kwargs)
        content_type = resp.getheader('content-type', None)

        if resp.status == 204 or resp.status == 205 or content_type is None:
            return resp, list()

        if 'application/json' in content_type:
            body = ''.join([chunk for chunk in body_iter])
            try:
                body = json.loads(body)
            except ValueError:
                LOG.error('Could not decode response body as JSON')
        else:
            body = None

        return resp, body

    def log_curl_request(self, method, url, kwargs):
        curl = ['curl -i -X %s' % method]

        for (key, value) in kwargs['headers'].items():
            header = '-H \'%s: %s\'' % (key, value)
            curl.append(header)

        if self.connection_params[2].get('insecure'):
            curl.append('-k')

        if 'body' in kwargs:
            curl.append('-d \'%s\'' % kwargs['body'])

        curl.append('%s%s' % (self.endpoint, url))
        LOG.debug(' '.join(curl))

    @staticmethod
    def log_http_response(resp, body=None):
        status = (resp.version / 10.0, resp.status, resp.reason)
        dump = ['\nHTTP/%.1f %s %s' % status]
        dump.extend(['%s: %s' % (k, v) for k, v in resp.getheaders()])
        dump.append('')

        if body:
            dump.extend([body, ''])
        LOG.debug('\n'.join(dump))

    def raw_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type',
                                     'application/octet-stream')
        return self._http_request(url, method, **kwargs)


class ResponseBodyIterator(object):
    """A class that acts as an iterator over an HTTP response."""

    def __init__(self, resp):
        self.resp = resp

    def __iter__(self):
        while True:
            yield self.next()

    def next(self):
        chunk = self.resp.read(CHUNKSIZE)
        if chunk:
            return chunk
        else:
            raise StopIteration()
