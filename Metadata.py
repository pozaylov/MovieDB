import enzyme


def mkv_metadata(file):
    """retrieve info from MKV's metadata file"""
    with open(file, 'rb') as f:
        mkv = enzyme.MKV(f)

    resolution = str(mkv.video_tracks[0].width) + 'x' + str(mkv.video_tracks[0].height)
    audio_channels = mkv.audio_tracks[0].channels
    runtime = str(mkv.info.duration).split('.', 1)[0]

    return {'resolution': resolution, 'audio_channels': audio_channels, 'runtime': runtime}

