from django.urls import path
from . import views

app_name = 'spectra'
urlpatterns = [
    path('', views.index, name='index'),

    # <collection_id> => views.collection
    # path('collection/<collection_id>/', views.collection, name='spectra_collection'),
    path('collection/', views.collection, name='collection'),
    path('spectrum/', views.spectra, name='spectrum'),
    path('collection/new', views.collection_new, name='collection_new'),
    path('spectrum/new', views.spectrum_new, name='spectrum_new'),
    path('get_spectra', views.get_spectra, name='get_spectra'),
    path('axios_spectra', views.get_spectra_axios, name='get_spectra_axios'),
    path('description_update', views.description_update, name='description_update'),
    path('change_permission', views.change_permission, name='change_permission'),
    path('export_from_list', views.export_from_list, name='export_from_list'),
    path('delete_from_list', views.delete_from_list, name='delete_from_list'),
]
