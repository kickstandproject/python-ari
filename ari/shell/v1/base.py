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

import logging

from cliff import command
from cliff import lister
from cliff import show

from ari.common import utils


class Command(command.Command):

    log = logging.getLogger(__name__ + '.Command')

    def __init__(self, app, app_args):
        super(Command, self).__init__(app, app_args)

    def get_client(self):
        return self.app.client_manager

    def get_data(self, parsed_args):
        pass

    def take_action(self, parsed_args):
        return self.get_data(parsed_args)


class ListCommand(Command, lister.Lister):

    list_columns = []
    log = None
    pagination = False
    resource = None
    sorting = False

    def _list(self, parsed_args):
        obj_lister = getattr(self.get_client(), self.resource)
        data = obj_lister.list()

        return data

    def get_data(self, parsed_args):
        self.log.debug(parsed_args)
        data = self._list(parsed_args)

        return self.setup_columns(data, parsed_args)

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        utils.add_show_list_common_argument(parser)

        if self.pagination:
            utils.add_pagination_argument(parser)

        if self.sorting:
            utils.add_sorting_argument(parser)

        return parser

    def setup_columns(self, info, parsed_args):
        _columns = len(info) > 0 and sorted(info[0].to_dict()) or []

        if not _columns:
            parsed_args.columns = []
        elif parsed_args.columns:
            _columns = [x for x in parsed_args.columns if x in _columns]
        elif self.list_columns:
            _columns = [x for x in self.list_columns if x in _columns]

        return (_columns, (utils.get_item_properties(
            s, _columns, ) for s in info), )


class ShowCommand(Command, show.ShowOne):

    allow_names = False
    log = None
    resource = None

    def _show(self, parsed_args):
        obj_shower = getattr(self.get_client(), self.resource)
        data = obj_shower.get(parsed_args.id)

        return data.to_dict()

    def get_data(self, parsed_args):
        self.log.debug(parsed_args)
        data = self._show(parsed_args)

        if not data:
            return ({}, {})
        else:
            return zip(*sorted(data.items()))

    def get_parser(self, prog_name):
        parser = super(ShowCommand, self).get_parser(prog_name)
        utils.add_show_list_common_argument(parser)

        if self.allow_names:
            help_str = 'ID or name of %s to look up'
        else:
            help_str = 'ID of %s to look up'

        parser.add_argument(
            'id', metavar=self.resource.upper(),
            help=help_str % self.resource)

        return parser
