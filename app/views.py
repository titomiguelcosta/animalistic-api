from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from app.permissions import HasAuthToken
from app.models import Photo
from app.serializers import PhotoSerializer
from rest_framework.decorators import action
# from picamera import PiCamera
from time import sleep
from django.conf import settings
import os
from datetime import datetime


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [HasAuthToken]

    @action(detail=False, methods=['post'])
    def take(self, request):
        filename = '%s.jpg' % datetime.now().strftime('%Y%m%d%H%M%S%f')
        # camera = PiCamera()
        # camera.resolution = (2592, 1944)
        # camera.saturation = -100
        # camera.sharpness = -100
        # camera.flash_mode = 'torch'
        # camera.image_effect = 'none'
        # camera.rotation = 270
        # camera.color_effects = (128, 128)
        # camera.brightness = 50
        # camera.contrast = 50
        # camera.awb_mode = 'shade'
        # camera.exposure_mode = 'antishake'
        # sleep(2)
        # camera.start_preview()
        # camera.capture(os.path.join(settings.MEDIA_ROOT, filename))
        # camera.stop_preview()

        photo = Photo()
        photo.name = filename
        photo.save()

        return Response(PhotoSerializer(photo).data)

    @action(detail=False, methods=['get'])
    def stream(self, request):
        camera = PiCamera()
        return StreamingHttpResponse(self.gen(camera))

    def gen(self, camera):
        while True:
            f = os.path.join('/tmp', 'stream.jpg')
            camera.resolution = (1024, 512)
            camera.capture(f)

            frame = open(f, 'rb').read()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )
