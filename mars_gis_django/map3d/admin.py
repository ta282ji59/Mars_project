from django.contrib import admin
from .models import SuperCam
from .models import SuperCamMeta

# Register your models here.
admin.site.register(SuperCam)
admin.site.register(SuperCamMeta)