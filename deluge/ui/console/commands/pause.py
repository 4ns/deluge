#!/usr/bin/env python
#
# pause.py
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
from deluge.ui.client import client
import deluge.ui.console.colors as colors

class Command(BaseCommand):
    """Pause a torrent"""
    usage = "Usage: pause [ all | <torrent-id> [<torrent-id> ...] ]"
    def handle(self, *args, **options):
        if len(args) == 0:
            print self.usage
            return
        if len(args) == 1 and args[0] == 'all':
            args = tuple() # empty tuple means everything
        try:
            args = mapping.to_ids(args)
            torrents = match_torrents(args)
            client.pause_torrent(torrents)
        except Exception, msg:
            print templates.ERROR(str(msg))
        else:
            print templates.SUCCESS('torrent%s successfully paused' % ('s' if len(args) > 1 else ''))

    def complete(self, text, *args):
        torrents = match_torrents()
        names = mapping.get_names(torrents)
        return [ x[1] for x in names if x[1].startswith(text) ]
