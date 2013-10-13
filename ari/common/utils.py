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

import argparse
import os

from ari.openstack.common import importutils


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def import_versioned_module(version, submodule=None):
    module = 'ari.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))

    return importutils.import_module(module)


def get_item_properties(item, fields, mixed_case_fields=[]):
    """Return a tuple containing the item properties.

    :param item: a single item resource (e.g. Server, Tenant, etc)
    :param fields: tuple of strings with the desired field names
    :param mixed_case_fields: tuple of field names to preserve case
    """
    row = []

    for field in fields:
        if field in mixed_case_fields:
            field_name = field.replace(' ', '_')
        else:
            field_name = field.lower().replace(' ', '_')
        if not hasattr(item, field_name) and isinstance(item, dict):
            data = item[field_name]
        else:
            data = getattr(item, field_name, '')
        if data is None:
            data = ''
        row.append(data)

    return tuple(row)


def add_pagination_argument(parser):
    parser.add_argument(
        '-P', '--page-size',
        dest='page_size', metavar='SIZE', type=int,
        help=("specify retrieve unit of each request, then split one request "
              "to several requests"),
        default=None)


def add_show_list_common_argument(parser):
    parser.add_argument(
        '-D', '--show-details',
        help='show detailed info',
        action='store_true',
        default=False, )
    parser.add_argument(
        '--show_details',
        action='store_true',
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--fields',
        help=argparse.SUPPRESS,
        action='append',
        default=[])
    parser.add_argument(
        '-F', '--field',
        dest='fields', metavar='FIELD',
        help='specify the field(s) to be returned by server,'
        ' can be repeated',
        action='append',
        default=[])
