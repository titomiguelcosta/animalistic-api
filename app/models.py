from django.db import models
from django.utils.timezone import now


class Photo(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)
    tags = models.ManyToManyField('Tag', through='PhotoTags')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class PhotoTags(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
