from app.models import Photo, Tag
from rest_framework import serializers


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Photo
        fields = ['id', 'name', 'created_at', 'tags', ]
