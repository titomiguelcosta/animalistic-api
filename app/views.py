from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from app.permissions import HasAuthToken
from app.models import Photo
from app.serializers import PhotoSerializer
from rest_framework.decorators import action
from app.services.camera import Camera
from django.conf import settings
import os
import io
from datetime import datetime
import logging


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [HasAuthToken]
    logger = logging.getLogger('django')

    @action(detail=False, methods=['post'])
    def take(self, request):
        filename = '%s.jpg' % datetime.now().strftime('%Y%m%d%H%M%S%f')

        Camera.initialize()
        Camera.camera.capture(os.path.join(
            settings.MEDIA_ROOT, filename),
            quality=100
        )

        photo = Photo()
        photo.name = filename
        photo.save()

        return Response(PhotoSerializer(photo).data)

    # @see https://github.com/miguelgrinberg/flask-video-streaming
    @action(detail=False, methods=['get'])
    def stream(self, request):
        Camera.initialize()

        return StreamingHttpResponse(self.gen(), content_type='multipart/x-mixed-replace; boundary=frame')

    def gen(self):
        for frame in self.frames():
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def frames(self):
        stream = io.BytesIO()
        for _ in Camera.camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            yield stream.read()

            stream.seek(0)
            stream.truncate()
