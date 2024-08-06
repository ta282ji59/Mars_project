from django.contrib import admin
from .models import Collection, Spectrum


class SpectrumAdmin(admin.ModelAdmin):
    list_display = ('user','instrument','data_id','latitude','longitude','created_date','permission')
    list_display_links = ('instrument','data_id','latitude','longitude','created_date','permission')

    def user_get(self, obj):
        return obj.user.username

admin.site.register(Collection)
admin.site.register(Spectrum, SpectrumAdmin)