#Mongo db
from guest_list.documents import *
from rest_framework_mongoengine import serializers as mongoserializers

class GuestSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'guest_id', 'email', 'name', 'phone', 'pax', 'plus_one', 'remarks', 'is_attending', 'confirmed']

class PhotoSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photo_id', 'src', 'height', 'width', 'is_carousel', 'is_event_cover']