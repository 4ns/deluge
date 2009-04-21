Deluge.Keys = {
    Grid: [
        'queue', 'name', 'total_size', 'state', 'progress', 'num_seeds',
        'total_seeds', 'num_peers', 'total_peers', 'download_payload_rate',
        'upload_payload_rate', 'eta', 'ratio', 'distributed_copies',
        'is_auto_managed', 'time_added', 'tracker_host'
    ],
    Status: [
        'total_done', 'total_payload_download', 'total_uploaded',
        'total_payload_upload', 'next_announce', 'tracker_status', 'num_pieces',
        'piece_length', 'is_auto_managed', 'active_time', 'seeding_time',
        'seed_rank'
    ],
    Files: [
        'files', 'file_progress', 'file_priorities'
    ],
    Peers: [
        'peers', 'seeds'
    ],
    Details: [
        'name', 'save_path', 'total_size', 'num_files', 'tracker_status',
        'tracker', 'comment'
    ],
    Options: [
        'max_download_speed', 'max_upload_speed', 'max_connections',
        'max_upload_slots','is_auto_managed', 'stop_at_ratio', 'stop_ratio',
        'remove_at_ratio', 'private', 'prioritize_first_last'
    ]
};

Ext.each(Deluge.Keys.Grid, function(key) {
    Deluge.Keys.Status.push(key);
});