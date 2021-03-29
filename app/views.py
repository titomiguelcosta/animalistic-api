from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app.permissions import HasAuthToken
from app.models import Photo
from app.serializers import PhotoSerializer
from rest_framework.decorators import action
from picamera import PiCamera
from time import sleep
from django.conf import settings
import os
from datetime import datetime


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [HasAuthToken]

    @action(detail=False, methods=['post'])
    def take():
        filename = '%s.jpg' % datetime.now().strftime('%Y%m%d%H%M%S%f')
        camera = PiCamera()
        camera.resolution = (2592, 1944)
        camera.saturation = -100
        camera.sharpness = -100
        camera.flash_mode = 'torch'
        camera.image_effect = 'none'
        camera.rotation = 270
        camera.color_effects = (128, 128)
        camera.brightness = 50
        camera.contrast = 50
        camera.awb_mode = 'shade'
        camera.exposure_mode = 'antishake'
        sleep(2)
        camera.capture(os.path.join(settings.MEDIA_ROOT, filename))

        photo = Photo()
        photo.filename = filename
        photo.save()

        return Response(photo)
