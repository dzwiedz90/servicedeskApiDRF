from django.contrib import admin

from .models import User, Case, CaseUpdate


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username',)
    search_fields = ['pk']


class CaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'severity')


class CaseUpdateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'case', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseUpdate, CaseUpdateAdmin)
