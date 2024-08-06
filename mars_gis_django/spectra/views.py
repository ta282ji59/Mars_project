from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, date
from . import forms, models
from spectra.models import Spectrum
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
import json, csv, os

@login_required
def index(request):
	settings = {
	}
	return render(request, "spectra/index.html", settings)

def convert_dygraphs_data(record_spectra):
    print("Execute convert_dygraphs_data.")

    dygraphs_spectra = []

    for j,spectrum in enumerate(record_spectra):
        data = []
        wavelengths = list(map(float, spectrum.wavelength.lstrip('[').rstrip(']').split(', ')))
        reflectances = list(map(float, spectrum.reflectance.lstrip('[').rstrip(']').split(', ')))

        # 逆順であれば直す
        if wavelengths[0] > wavelengths[-1]:
            wavelengths.reverse()
            reflectances.reverse()

        for (wav, ref) in zip(wavelengths, reflectances):
            pair = [wav, ref]
            data.append(pair)

        dygraphs_spectra.append({
            "data": data,
            "id_graph": "graph" + str(j),
            "id_map": "map" + str(j),
            "rec": spectrum
        })

    return dygraphs_spectra


from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
def spectra(request):
    user_id = request.user.id
    # user = get_object_or_404(User, pk=user_id)
    user = get_object_or_404(get_user_model(), pk=user_id)
    spectra = user.spectrum_set.all()
    dygraphs_spectra = convert_dygraphs_data(spectra)
    settings = {
        'user': user,
        'spectra': spectra,
        'dygraphs_spectra': dygraphs_spectra,
    }
    return render(request, "spectra/spectra.html", settings)

from decimal import Decimal


def get_spectra(request):
    if request.method == "GET":
        user_id = request.user.id
        user = get_object_or_404(get_user_model(), pk=user_id)
        spectra = request.user.spectrum_set.all()
        dygraphs_spectra = convert_dygraphs_data(spectra)
        settings = {
            'user': user,
            'spectra': spectra,
            'dygraphs_spectra': dygraphs_spectra,
        }
        return settings


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Spectrum):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, (datetime, date)):
            return str(obj)
        # elif isinstance(obj, User):
        elif isinstance(obj, get_user_model()):
            return str(obj)
        else:
            raise TypeError(
                "Unserializable object {} of type {}".format(obj, type(obj))
            )


def get_spectra_axios(request):
    if request.method == "GET" or json.loads(request.body)["selected"] == "my_all":
        print("agagagagagag")

        user = request.user
        spectra = models.Spectrum.objects.filter(user=user).order_by('-id')
        dygraphs_spectra = convert_dygraphs_data(spectra)

        spectra_list = []
        coordinate_list = []
        for j,spectrum in enumerate(spectra):
            spectra_list.append({
                "instrument": spectrum.instrument, 
                "obs_id": spectrum.obs_id, 
                "path": spectrum.path,
                "image_path": spectrum.image_path,
                "x_pixel": spectrum.x_pixel, 
                "y_pixel": spectrum.y_pixel, 
                "mineral_id": spectrum.mineral_id,
                "description": spectrum.description, 
                "latitude": round(spectrum.latitude, 6), 
                "longitude": round(spectrum.longitude, 6),
                "created_date": spectrum.created_date.strftime("%Y/%m/%d %H:%M:%S"), 
                "user": spectrum.user,
                "permission": spectrum.permission, 
                "data_id": spectrum.data_id, 
                "id": spectrum.id, 
                "id_edit": "edit" + str(spectrum.id),
                "id_update": "update" + str(spectrum.id), 
                "id_accordion": "accordion" + str(spectrum.id), 
                "id_permission": "permission" + str(spectrum.id),
                "id_export": "export" + str(spectrum.id), 
                "id_delete": "delete" + str(spectrum.id), 
                "id_thumbnail": "thumbnail" + str(spectrum.id),
            })

        settings = {
            'spectra_list': spectra_list,
            'dygraphs_spectra': dygraphs_spectra,
        }
        json_list = json.dumps(settings, cls=LazyEncoder)
        return JsonResponse(json_list, safe=False)

    else:
        print("get_spectra_axios:post")
        print(json.loads(request.body)["selected"])
        filter_grp = json.loads(request.body)["selected"]

        if filter_grp == "private":
            user = request.user
            print(user)
            spectra = models.Spectrum.objects.filter(user=user).filter(permission=filter_grp)

            dygraphs_spectra = convert_dygraphs_data(spectra)

            spectra_list = []
            coordinate_list = []
            for j,spectrum in enumerate(spectra):
                spectra_list.append({
                    "instrument": spectrum.instrument, 
                    "obs_id": spectrum.obs_id, 
                    "path": spectrum.path,
                    "image_path": spectrum.image_path,
                    "x_pixel": spectrum.x_pixel, 
                    "y_pixel": spectrum.y_pixel, 
                    "mineral_id": spectrum.mineral_id,
                    "description": spectrum.description, 
                    "latitude": spectrum.latitude, 
                    "longitude": spectrum.longitude,
                    "created_date": spectrum.created_date.strftime("%Y/%m/%d %H:%M:%S"), 
                    "user": spectrum.user,
                    "permission": spectrum.permission, 
                    "data_id": spectrum.data_id, 
                    "id": spectrum.id, 
                    "id_edit": "edit" + str(spectrum.id),
                    "id_update": "update" + str(spectrum.id), 
                    "id_accordion": "accordion" + str(spectrum.id), 
                    "id_permission": "permission" + str(spectrum.id),
                    "id_delete": "delete" + str(spectrum.id), 
                    "id_thumbnail": "thumbnail" + str(spectrum.id)
                })
            settings = {
                'spectra_list': spectra_list,
                'dygraphs_spectra': dygraphs_spectra,
            }
            json_list = json.dumps(settings, cls=LazyEncoder)

            return JsonResponse(json_list, safe=False)


        else:
            spectra = models.Spectrum.objects.filter(permission=filter_grp)

            print(spectra)

            dygraphs_spectra = convert_dygraphs_data(spectra)

            spectra_list = []
            coordinate_list = []
            for j,spectrum in enumerate(spectra):
                spectra_list.append({
                    "instrument": spectrum.instrument, 
                    "obs_id": spectrum.obs_id, 
                    "path": spectrum.path,
                    "image_path": spectrum.image_path,
                    "x_pixel": spectrum.x_pixel, 
                    "y_pixel": spectrum.y_pixel, 
                    "mineral_id": spectrum.mineral_id,
                    "description": spectrum.description, 
                    "latitude": spectrum.latitude, 
                    "longitude": spectrum.longitude,
                    "created_date": spectrum.created_date.strftime("%Y/%m/%d %H:%M:%S"), 
                    "user": spectrum.user,
                    "permission": spectrum.permission, 
                    "data_id": spectrum.data_id, 
                    "id": spectrum.id, 
                    "id_edit": "edit" + str(spectrum.id),
                    "id_update": "update" + str(spectrum.id), 
                    "id_accordion": "accordion" + str(spectrum.id), 
                    "id_permission": "permission" + str(spectrum.id),
                    "id_thumbnail": "thumbnail" + str(spectrum.id)
                })

            settings = {
                'spectra_list': spectra_list,
                'dygraphs_spectra': dygraphs_spectra,
            }
            json_list = json.dumps(settings, cls=LazyEncoder)

            return JsonResponse(json_list, safe=False)


def change_permission(request):
    print("change_permission")

    if request.method == "POST":
        data_content = request.body.decode("utf-8")
        params_list = json.loads(data_content)
        print(params_list)
        permission_new = params_list["change_to"]
        print(permission_new)
        id = params_list["id_permission"].lstrip("permission")
        print(id)
        models.Spectrum.objects.filter(id=id).update(permission = permission_new)

        settings = {
            'permission': permission_new,
        }

        return render(request, "spectra/spectrum_new.html", settings)
    
def export_from_list(request):
    print("Execute export_from_list.")

    if request.method == "POST":
        export_list = json.loads(request.body.decode("utf-8"))

        for param in export_list:
            destination = param["destination"]
            csv_filename = param["csv_filename"]
            if destination == "private":
                export_path = f"/data/users/{request.user}/{csv_filename}"
            else:
                export_path = f"/data/groups/{destination}/{csv_filename}"

            with open(export_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(param["graph_data"])

        return HttpResponse("Success delete_from_list")

def delete_from_list(request):
    print("Execute delete_from_list.")

    if request.method == "POST":
        delete_list = json.loads(request.body.decode("utf-8"))

        for param in delete_list:
            Spectrum.objects.get(data_id=param["data_id"]).delete()
            print("Execute delete_from_list.x")

        return HttpResponse("Success delete_from_list")

###usui, 準備中
@login_required
def collection(request):
    user_id = request.user.id
    group = request.user.groups.filter(user=user_id)[0]
    collection = group.collection_set.all()[0] 
    spectra = collection.spectra.all()  
    dygraphs_spectra = convert_dygraphs_data(spectra) 

    settings = {
        'collection': collection, 
        'spectra': spectra, 
        'dygraphs_spectra': dygraphs_spectra, 
    }
    return render(request, "spectra/collection.html", settings)



def collection_edit(request):
		settings = {
			'form': forms.NewCollectionForm(),
		}
		return render(request, "spectra/collection_new.html", settings)

@login_required
def collection_new(request):
	if request.method == "POST":
		description = request.POST.get("description")
		owner = request.POST.get("owner")
		date = datetime.now()
		new_rec = models.Collection.objects.create(created_date=date,
										description=description,
										owner=owner)
		return redirect("/spectra/collection/"+str(new_rec.id))
	else:
		settings = {
			'form': forms.NewCollectionForm(),
		}
		return render(request, "spectra/collection_new.html", settings)


from django.contrib.gis.geos import GEOSGeometry, Point
from django.utils import timezone

@login_required
def spectrum_new(request):
    if request.method == "POST":

        print("spectrum_new here!!!")
        data_content = request.body.decode("utf-8")
        params_list = json.loads(data_content)
        new_records = []
        user = get_object_or_404(get_user_model(), pk=request.user.id)
        description = params_list["description"]

        for params_json in params_list["spectral_data"]:
            instrument = params_json["obs_name"]
            obs_id = params_json["obs_ID"]
            path = params_json["path"]
            image_path = params_json["Image_path"]
            x_pixel = params_json["pixels"][0]
            y_pixel = params_json["pixels"][1]
            x_image_size = params_json["Image_size"][0]
            y_image_size = params_json["Image_size"][1]
            wavelength = params_json["band_bin_center"]
            reflectance = params_json["reflectance"]
            longitude = params_json["coordinate"][0]
            latitude = params_json["coordinate"][1]
            point = GEOSGeometry('Point(%s %s)' %(longitude, latitude))
            created_date = timezone.datetime.now()
            data_id = f"{user}{instrument}{obs_id}{longitude}{latitude}{created_date.strftime('%Y-%m-%d-%H:%M:%S')}"

            new_rec = models.Spectrum(
                obs_id = obs_id,
                instrument = instrument,
                path = path,
                image_path = image_path,
                x_pixel = x_pixel,
                y_pixel = y_pixel,
                x_image_size = x_image_size,
                y_image_size = y_image_size,
                wavelength = wavelength,
                reflectance = reflectance,
                # mineral_id = mineral_id,
                latitude = latitude,
                longitude = longitude,
                point = point,
                user = user,
                description = description,
                created_date = created_date,
                data_id = data_id,
            )
            new_records.append(new_rec)

        models.Spectrum.objects.bulk_create(new_records)

        return redirect("/accounts/home")
    else:
        settings = {
            'form': forms.NewSpectrumForm(),
        }
        return render(request, "spectra/spectrum_new.html", settings)


from django.db.models import F
from decimal import Decimal
def description_update(request):
    print("AAAAAAAAAA")
    if request.method == "POST":
        data_content = request.body.decode("utf-8")
        params_list = json.loads(data_content)
        print(params_list)
        description = params_list["description"]
        print(description)
        id = params_list["id_update"].lstrip("update")
        print(id)
        models.Spectrum.objects.filter(id=id).update(description = description)

        settings = {
            'description': description,
        }

        return render(request, "spectra/spectrum_new.html", settings)
