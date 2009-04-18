#!/usr/bin/env python
#
# rm.py
#
# Copyright (C) 2008-2009 Ido Abramovich <ido.deluge@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA    02110-1301, USA.
#
from deluge.ui.console.main import BaseCommand, match_torrents
from deluge.ui.console import mapping
import deluge.ui.console.colors as colors
from deluge.ui.client import client
from optparse import make_option
import os

class Command(BaseCommand):
    """Remove a torrent"""
    usage = "Usage: rm <torrent-id>"
    aliases = ['del']

    option_list = BaseCommand.option_list + (
            make_option('--remove_data', action='store_true', default=False,
                        help="remove the torrent's data"),
    )

    def handle(self, *args, **options):
        try:
            args = mapping.to_ids(args)
            torrents = match_torrents(args)
            client.remove_torrent(torrents, options['remove_data'])
        except Exception, msg:
            print template.ERROR(str(msg))

    def complete(self, text, *args):
        torrents = match_torrents()
        names = mapping.get_names(torrents)
        return [ x[1] for x in names if x[1].startswith(text) ]
