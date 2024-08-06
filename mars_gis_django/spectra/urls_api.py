from django.urls import include
from django.conf.urls import url

from . import apis

urlpatterns = [
    url('',include(apis.router.urls)),
]