
from django.contrib import admin

from .models import Advert, Response, Category


class AdvertAdmin(admin.ModelAdmin):
    """ Admin panel upgrade """
    list_display = ('id', 'author', 'title', 'text', 'category', 'createTime', 'editTime', 'upload', )
    search_fields = ('title', 'text', 'author', )
    list_filter = ('id', 'author', 'title', 'text', 'category', 'createTime', 'editTime', )


class ResponseAdmin(admin.ModelAdmin):
    """ Admin panel upgrade """
    list_display = [field.name for field in Response._meta.get_fields()]


class CategoryAdmin(admin.ModelAdmin):
    """ Admin panel upgrade """
    list_display = ('text', )


admin.site.register(Advert, AdvertAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Category, CategoryAdmin)
