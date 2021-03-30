from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from app.permissions import HasAuthToken
from app.models import Photo
from app.serializers import PhotoSerializer
from rest_framework.decorators import action
from picamera import PiCamera
from time import sleep
from django.conf import settings
import os
import io
from datetime import datetime


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [HasAuthToken]

    @action(detail=False, methods=['post'])
    def take(self, request):
        filename = '%s.jpg' % datetime.now().strftime('%Y%m%d%H%M%S%f')

        camera = self._camera()
        camera.capture(os.path.join(settings.MEDIA_ROOT, filename))
        camera.close()

        photo = Photo()
        photo.name = filename
        photo.save()

        return Response(PhotoSerializer(photo).data)

    # @see https://github.com/miguelgrinberg/flask-video-streaming
    @action(detail=False, methods=['get'])
    def stream(self, request):
        return StreamingHttpResponse(self.gen(), content_type='multipart/x-mixed-replace; boundary=frame')

    def gen(self):
        for frame in self.frames():
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def frames(self):
        camera = self._camera()
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            yield stream.read()

            stream.seek(0)
            stream.truncate()

        camera.close()

    def _camera(self):
        camera = PiCamera()
        camera.resolution = (1024, 768)
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
        # give time to calibrate
        sleep(2)

        return camera
