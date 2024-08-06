from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from spectra.models import Spectrum
# from django.views.generic import TemplateView
from django.core.serializers import serialize
# from djgeojson.serializers import Serializer as GeoJSONSerializer
from accounts.models import CustomUser
from accounts.models import Project

# TODO SuperCam閲覧機能 2024/3/1(kuro)
# from map3d.models import SuperCam
# from map3d.models import SuperCamMeta
# from django.http import JsonResponse
# import json

# def create_geojson():
#     spectra = Spectrum.objects.all()
#
#     for j,spectrum in enumerate(spectra):
#         if j==0:
#             geojson = {
#                 "type": "FeatureCollection",
#                 "crs": {
#                     "type": "name",
#                     "properties": {
#                         "name": "EPSG:4326"
#                     }
#                 },
#                 "features": [
#                     {
#                         "type": "Feature",
#                         "properties": {
#                             "instrument": "THEMIS"
#                         },
#                         "geometry": {
#                             "type": "Point",
#                             "coordinates": [
#                                 -73.8047144010574,
#                                 30.80614948603047
#                             ]
#                         }
#                     }
#         # else:
#         #     rec =
#
#     #
#     geojson="a"
#     return geojson


from spectra.views import get_spectra

# @login_required
def default(request):
    if request.user.is_authenticated:
        # geo_json = serialize('geojson', Spectrum.objects.all(),
        user = request.user
        geo_json = serialize('geojson', Spectrum.objects.filter(user=user),
            geometry_field='point',
            # pk='NOTE',
            # title='Note',
            # name='Note',
            # fields=('instrument','description',) 
            fields=('description',) 
        )

        rec_spectra = get_spectra(request)

        rec = {
            'name': "Note",
            'title': "Note",
            'geojson': geo_json,
        }
        rec_for_jump = []
        for j,spectrum in enumerate(rec_spectra["spectra"]):
            # print(spectrum.latitude)
            # rec_for_jump = []
            record = {
                'N': 3,
                # 'id': spectrum["dygraphs_spectra"]["rec"]["id"],
                # 'lat': spectrum["dygraphs_spectra"]["rec"]["latitude"],
                # 'lon': spectrum["dygraphs_spectra"]["rec"]["longitude"],
                'id': spectrum.id,
                'lat': float(spectrum.latitude),
                'lon': float(spectrum.longitude),
                'zoom': 15000000,
                # 'geojson': geo_json,
            }
            rec_for_jump.append(record)
        user = request.user

        # TODO:usui231228
        user_id = request.user.id
        projects = Project.objects.filter(member__in=[user_id])
        # user_info = CustomUser.objects.get(id=1)
        # participated_projects = CustomUser.Project.all()

        # TODO SuperCam閲覧機能 2024/3/1(kuro)
        # Supercamのレコードを取得する
        # sol_list = SuperCam.objects.values_list('sol', flat=True).distinct()

        settings = {
            'record_json': rec,
            'record_spectra': rec_spectra,
            'record_jump': rec_for_jump, 
            'projects': projects, 
            # 'dygraphs_spectra': rec_spectra["dygraphs_spectra"],
            # 'record': rec_spectra["dygraphs_spectra"]
            'user': user,
            # 'spectra': spectra,
            # 'dygraphs_spectra': dygraphs_spectra,

            # TODO SuperCam閲覧機能 2024/3/1(kuro)
            # 'sol_list': sol_list
        }

        return render(request, "map3d/index.html", settings)
    else:
        return render(request, "map3d/login.html")




##############################
### 入力した緯度経度地点に飛ぶ ###
##############################
from spectra.models import Spectrum
# from django.contrib.gis.geos import GEOSGeometry, Point
def jump(request):
    # # id = request.body.decode('utf-8')
    # id = request.session.get("test")
    id = request.POST["id"]
    spectrum = get_object_or_404(Spectrum, pk = int(id))
    rec = {
        'id': id,
        'N': 4,
        'lat': spectrum.latitude,
        'lon': spectrum.longitude,
        'zoom': 15000000,
        'point': spectrum.point,
        # 'spectrum': spectrum,
    }
    settings = {
        'record_json': rec,
    }
    # return render(request, "map3d/test.html", settings)
    return render(request, "map3d/index.html", settings)



# from djgeojson.views import GeoJSONLayerView
# from django.views.generic import TemplateView
from django.core.serializers import serialize
def test_gis(request):
    geo_json = serialize('geojson', Spectrum.objects.all(),
            geometry_field='point',
            fields=('instrument','description',))
    settings = {
        'geo_json': geo_json,
    }
    # return render(request, "map3d/test2.html", settings)
    return render(request, "map3d/index.html", settings)


# TODO SuperCam閲覧機能 2024/3/1(kuro)
# リクエストのIDからsupercamのデータを取得し、json形式に変換する
# def convertSuperCam(request):
#     if request.is_ajax():
#         selected_id = request.GET.get('id', None)

#         # データベースからデータを検索
#         data = SuperCam.objects.get(pk=int(selected_id))

#         # コンマ区切りの文字列を配列に変換
#         wavelength = [float(x) for x in data.csv_wavelength.split(',')]
#         reflectance = [float(x) for x in data.csv_reflectance.split(',')]

#         # json形式に変換
#         supercam_json = {
#             'Image_path': '', 
#             'Image_size' : [],
#             'band_bin_center' : wavelength,
#             'band_number' : len(wavelength),
#             'coordinate' : [data.longitude, data.latitude],
#             'obs_ID' : data.obs_id, 
#             'obs_name' : 'SuperCam',
#             'path' : '',
#             'pixels' : [],
#             'reflectance' : reflectance,
#             'type': 'DIRECT'
#         }
        
#         supercam_meta = SuperCamMeta.objects.get(file_name__exact=data.file_name)

#         supercam_meta_json = {
#             'file_name' : supercam_meta.file_name, 
#             'product_class' : supercam_meta.product_class,
#             'title' : supercam_meta.title,
#             'version_id' : supercam_meta.version_id,
#             'local_mean_solar_time' : supercam_meta.local_mean_solar_time,
#             'local_true_solar_time' : supercam_meta.local_true_solar_time,
#             'processing_level' : supercam_meta.processing_level,
#             'solar_longitude': supercam_meta.solar_longitude,
#             'solar_longitude_unit' : supercam_meta.solar_longitude_unit,
#             'start_date_time' : supercam_meta.start_date_time,
#             'stop_date_time' : supercam_meta.stop_date_time
#         }

#         response_data = {
#             'supercam' : supercam_json, 
#             'supercam_meta' : supercam_meta_json
#         }

#         return JsonResponse(response_data)
#     else:
#         return render(request, 'map3d/index.html')

# def searchSuperCam(request):
#     if request.is_ajax():
#         min_lat = float(request.GET.get('min_lat', None))
#         max_lat = float(request.GET.get('max_lat', None))
#         min_lon = float(request.GET.get('min_lon', None))
#         max_lon = float(request.GET.get('max_lon', None))

#         # SuperCamモデルを直接検索
#         super_cams_in_range = SuperCam.objects.filter(
#             latitude__range=(min_lat, max_lat),
#             longitude__range=(min_lon, max_lon)
#         )

#         super_cams_data = [{'id': super_cam.id, 'file_name': super_cam.file_name} for super_cam in super_cams_in_range]

#         response_data = {'supercams': super_cams_data}

#         return JsonResponse(response_data, safe=False)
#     else:
#         return JsonResponse({})
    
# def searchSupercamBySol(request):
#     if request.is_ajax():
#         sol = request.GET.get('sol', None)
#         supercams = SuperCam.objects.filter(sol=sol)
#         supercam_list = [{'id': supercam.id, 'file_name': supercam.file_name, } for supercam in supercams]
#         return JsonResponse({'supercams': supercam_list})
#     else:
#         return JsonResponse({})
