from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, RelationshipFrom,
                      DateTimeFormatProperty, FloatProperty, StructuredRel,
                      BooleanProperty, DateProperty)

class TrackRel(StructuredRel):
    count = IntegerProperty(unique_index=False, required=True)

class Track(StructuredNode):
    uid = UniqueIdProperty()
    tag_id = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)

class Channel(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    body = StringProperty()
    created = DateProperty()
    image = StringProperty()
    is_featured = BooleanProperty(default=False)
    link = StringProperty()
    slug = StringProperty(unique_index=True)
    updated = DateProperty()
    follows = RelationshipTo('Channel', 'FOLLOWS')
    likes = RelationshipTo(Track, 'LIKES')
