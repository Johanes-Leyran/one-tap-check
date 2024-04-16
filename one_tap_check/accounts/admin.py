from django.contrib import admin
from .models.account import OneTapUser
from .models.tag import Tag

admin.site.register(OneTapUser)
admin.site.register(Tag)
