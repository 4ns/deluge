#!/usr/bin/env python
#
# info.py
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
#from deluge.ui.console.colors import templates
from deluge.ui.client import client
import deluge.common as common
from optparse import make_option

status_keys = ["state",
        "save_path",
        "tracker",
        "next_announce",
        "name",
        "total_size",
        "progress",
        "num_seeds",
        "total_seeds",
        "num_peers",
        "total_peers",
        "eta",
        "download_payload_rate",
        "upload_payload_rate",
        "ratio",
        "distributed_copies",
        "num_pieces",
        "piece_length",
        "total_done",
        "files",
        "file_priorities",
        "file_progress",
        "peers",
        "is_seed",
        ]


class Command(BaseCommand):
    """Show information about the torrents"""

    option_list = BaseCommand.option_list + (
            make_option('-v', '--verbose', action='store_true', default=False, dest='verbose',
                        help='shows more information per torrent'),
            make_option('-i', '--id', action='store_true', default=False, dest='tid',
                        help='use internal id instead of torrent name'),
    )

    usage =  "Usage: info [<torrent-id> [<torrent-id> ...]]\n"\
             "       You can give the first few characters of a torrent-id to identify the torrent."


    def handle(self, *args, **options):
        def on_to_ids(result):
            def on_match_torrents(torrents):
                for torrent in torrents:
                    self.show_info(torrent, options.get("verbose"))

            match_torrents(result).addCallback(on_match_torrents)
        mapping.to_ids(args).addCallback(on_to_ids)

#    def complete(self, text, *args):
#        torrents = match_torrents()
#        names = mapping.get_names(torrents)
#        return [ x[1] for x in names if x[1].startswith(text) ]

    def show_info(self, torrent, verbose):
        def _got_torrent_status(state):
            print templates.info_general('ID', torrent)
            print templates.info_general('Name', state['name'])
            #self._mapping[state['name']] = torrent # update mapping
            print templates.info_general('Path', state['save_path'])

            if verbose or not state['is_seed']:
                print templates.info_transfers("Completed", common.fsize(state['total_done']) + "/" + common.fsize(state['total_size']))
            print templates.info_transfers("Status", state['state'])

            if verbose or state['state'] == 'Downloading':
                print templates.info_transfers("Download Speed", common.fspeed(state['download_payload_rate']))
            if verbose or state['state'] in ('Downloading', 'Seeding'):
                print templates.info_transfers("Upload Speed", common.fspeed(state['upload_payload_rate']))
                print templates.info_transfers("Share Ratio", "%.1f" % state['ratio'])
            if state['state'] == ('Downloading'):
                print templates.info_transfers("ETA", common.ftime(state['eta']))

            if verbose:
                print templates.info_network("Seeders", "%s (%s)" % (state['num_seeds'], state['total_seeds']))
                print templates.info_network("Peers", "%s (%s)" % (state['num_peers'], state['total_peers']))
                print templates.info_network("Availability", "%.1f" % state['distributed_copies'])
                print templates.info_files_header("Files")
                for i, file in enumerate(state['files']):
                    status = ""
                    if not state['is_seed']:
                        if state['file_priorities'][i] == 0:
                            status = " - Do not download"
                        else:
                            status = " - %1.f%% completed" % (state['file_progress'][i] * 100)
                    print "\t* %s (%s)%s" % (file['path'], common.fsize(file['size']), status)

                print templates.info_peers_header("Peers")
                if len(state['peers']) == 0:
                    print "\t* None"
                for peer in state['peers']:
                    client_str = unicode(peer['client'])
                    client_str += unicode(peer['seed']) if peer['seed'] else ''
                    print templates.info_peers(str(peer['ip']), unicode(client_str),
                                        str(common.fspeed(peer['up_speed'])), str(common.fspeed(peer['down_speed'])))
            print ""
        client.core.get_torrent_status(torrent, status_keys).addCallback(_got_torrent_status)
