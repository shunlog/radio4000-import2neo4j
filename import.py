import json
import models
import datetime
import os
from tqdm import tqdm
from neomodel import config
from models import (Track, Channel, TrackRel)

config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]

with open('tmp/channels.json', 'r') as f:
    channels = json.load(f)

# for channel in channels:
#     print(json.dumps(channels[channel], indent=4))

# print(json.dumps(channels, indent=4))

its = 10

keys = channels.keys()
for uid in tqdm(keys):
    title = channels[uid].get('title', 'Default title')
    body = channels[uid].get('body', None)
    created = datetime.datetime.fromtimestamp(channels[uid].get('created', 0)//1000).date()
    image = channels[uid].get('image', None)
    is_featured = channels[uid].get('is_featured', False)
    link = channels[uid].get('link', None)
    slug = channels[uid].get('slug', None)
    updated = datetime.datetime.fromtimestamp(channels[uid].get('updated', 0)//1000).date()
    follows = channels[uid].get('follows', None)
    likes = channels[uid].get('likes', None)

    channel = models.Channel(title=title, body=body, created=created, image=image,
                    is_featured=is_featured, link=link, slug=slug,
                    updated=updated, follows=follows, likes=likes)
    print(channel)
    channel.save()

    if its <= 0:
        break
    its -= 1
