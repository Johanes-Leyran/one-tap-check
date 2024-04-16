from django.contrib import admin
from .models.account import OneTapUser
from .models.tag import Tag


class ShowPKAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)


admin.site.register(OneTapUser, ShowPKAdmin)
admin.site.register(Tag, ShowPKAdmin)
