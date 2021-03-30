from picamera import PiCamera
from django.core.signals import request_finished
from django.dispatch import receiver
from time import sleep


class Camera():
    camera = None

    @staticmethod
    def initialize():
        camera = PiCamera() if Camera.camera is None else Camera.camera
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

        Camera.camera = camera

        return Camera.camera

    @receiver(request_finished)
    def close(sender, **kwargs):
        if Camera.camera is not None:
            Camera.camera.close()
            Camera.camera = None
