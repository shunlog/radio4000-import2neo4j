import json
import models
import datetime
import os
import uuid
import re
from itertools import islice
from tqdm import tqdm
from neomodel import config
from models import (Track, Channel, Tag, TagRel)


def get_channel_from_dict(channel_dict):
    title = channel_dict.get('title')
    body = channel_dict.get('body', None)
    created_timestamp = channel_dict.get('created', 0)//1000
    created = datetime.datetime.fromtimestamp(created_timestamp).date()
    image = channel_dict.get('image', None)
    is_featured = channel_dict.get('isFeatured', False)
    link = channel_dict.get('link', None)
    slug = channel_dict.get('slug', None)
    updated_timestamp = channel_dict.get('updated', 0)//1000
    updated = datetime.datetime.fromtimestamp(updated_timestamp).date()
    return models.Channel(title=title, body=body, created=created, image=image,
                          is_featured=is_featured, link=link, slug=slug,
                          updated=updated)


def get_track_from_dict(track_dict):
    title = track_dict.get('title')
    url = track_dict.get('url')
    body = track_dict.get('body')
    discogs_url = track_dict.get('discogsUrl')
    media_not_available = track_dict.get('mediaNotAvailable', False)
    created_timestamp = track_dict.get('created', 0)//1000
    created = datetime.datetime.fromtimestamp(created_timestamp).date()
    return models.Track(title=title, url=url, discogs_url=discogs_url,
                        media_not_available=media_not_available,
                        created=created)


def import_from_json(channels, tracks):
    regex = re.compile(r'#[\w-]+\s')
    tags = {}
    tracks_map = {}
    keys = channels.keys()
    start = 100
    stop = 200
    for uid in tqdm(islice(keys, start, stop)):
        channel = get_channel_from_dict(channels[uid])
        channel.save()

        tracks_list = channels[uid].get('tracks')
        if not tracks_list:
            continue
        for track_id in tqdm(tracks_list.keys()):
            url = tracks[track_id]['url']
            if not url:
                continue
            if url in tracks_map.keys():
                track = tracks_map[url]
            else:
                track = get_track_from_dict(tracks[track_id])
                track.save()
                tracks_map[url] = track
            track_rel = channel.likes.connect(track)
            track_body = tracks[track_id].get('body')
            if not track_body:
                continue
            track_rel.body = track_body
            track_rel.save()

            for tag_name in regex.findall(track_body):
                tag_name = tag_name.strip()[1:]  # get rid of '#'
                if tag_name in tags.keys():
                    tag = tags[tag_name]
                else:
                    tag = models.Tag(name=tag_name)
                    tag.save()
                    tags[tag_name] = tag
                    track.tags.connect(tag, {'channel': channel.uid})

    for uid in tqdm(islice(keys, start, stop)):
        slug = channels[uid]['slug']
        channel = models.Channel.nodes.get_or_none(slug=slug)
        if not channel:
            continue
        followed_ls = channels[uid].get('favoriteChannels')
        if not followed_ls:
            continue
        for followed_id in followed_ls:
            channel_followed_dict = channels.get(followed_id)
            if not channel_followed_dict:
                continue
            followed_slug = channel_followed_dict['slug']
            channel_followed = models.Channel.nodes.get_or_none(slug=followed_slug)
            if not channel_followed:
                continue
            channel.follows.connect(channel_followed)



if __name__=="__main__":
    config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]
    with open('tmp/channels.json', 'r') as f:
        channels = json.load(f)
    with open('tmp/tracks.json', 'r') as f:
        tracks = json.load(f)
    import_from_json(channels, tracks)
