from django.contrib import admin
from .models.account import OneTapUser
from .models.tag import Tag


class OneTapAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)
    search_fields = ('last_name', 'email', 'pk',)


class ShowPKAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)
    search_fields = ('pk',)


admin.site.register(OneTapUser, OneTapAdmin)
admin.site.register(Tag, ShowPKAdmin)
