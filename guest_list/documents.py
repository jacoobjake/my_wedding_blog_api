# Mongo DB Document Class
from mongoengine import *

PLUS_ONE_CHOICES = ["FAMILY", "PLUS_ONE", "NONE"]

# Create your models here.
class Guest(Document):
    guest_id = SequenceField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(blank=True, auto_now=True)
    name = StringField(max_length=100, blank=True, default='')
    email = StringField(blank=True, null=True)
    phone = StringField(blank=True, null=True)
    pax = IntField(default=0)
    plus_one = StringField(max_length=100, blank=True, default='')
    is_attending = BooleanField(default=False)
    confirmed = BooleanField(default=False)
    remarks = StringField(blank=True, null=True)

    class Meta:
        ordering = ['created']

class Photo(Document):
    photo_id = SequenceField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(blank=True, auto_now=True)
    src = StringField(required=True)
    width = IntField(required=True)
    height = IntField(required=True)
    is_carousel = BooleanField(default=False)
    is_event_cover = BooleanField(default=False)
