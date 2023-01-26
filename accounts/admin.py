
from django.contrib import admin

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    """ Admin panel Token """
    list_display = [field.name for field in Token._meta.get_fields()]


admin.site.register(Token, TokenAdmin)

