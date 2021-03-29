from app.models import Photo, Tag
from rest_framework import serializers


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Photo
        fields = ['name', 'created_at', 'tags', ]
