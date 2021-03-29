from django.contrib import admin
from app.models import Photo, Tag


class PhotoAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tag, TagAdmin)
