import cgitb
cgitb.enable()

import psycopg2
import json
import collections as cl
# import cgi
# import os
# import sys
# import glob
# import pvl
# import numpy as np
# from osgeo import gdal,osr
# from itertools import product
# from pyproj import Proj, transform

#これやれchmod 755 api_json_db.py
print('api_db')

#========================json用関数=======================================
def json_construction(result,layer):
    observation_id = []
    path = []
    footprint = []
    for row in result:
        observation_id.append(row[0])
        footprint.append(row[1])
        path.append(row[2])
        pass

    feature_list = []
    for Dict_i in range(len(observation_id)):
        field_properties = cl.OrderedDict()
        field_properties["id"] = observation_id[Dict_i]
        field_properties["name"] = layer

        try:
            field_properties["path"] = json.loads(path[Dict_i])
        except Exception as e:
            field_properties["path"] = path[Dict_i]

        field_features = cl.OrderedDict()
        field_features["type"] = "Feature"
        field_features["geometry"] = json.loads(footprint[Dict_i])
        field_features["properties"] = field_properties
        feature_list.append(field_features)

    field_hit_data = cl.OrderedDict()
    field_hit_data["type"] = "FeatureCollection"
    field_hit_data["features"] = feature_list
    hit_data_list = []
    hit_data_list.append(field_hit_data)
    return hit_data_list

#==========================データベース接続=============================
def db_connect(params_json):
    hit_data_list2 = []
    lat = params_json["X"]
    lon = params_json["Y"]
    layers = []
    layers = params_json["QUERY_LAYERS"]
    search_radius = params_json["RADIUS_CIRCLE"]
    dbname = "mars"
    info = "host=172.16.238.5 dbname=%s user=verethragna password=mischief" %(dbname)
    # info = "host = localhost dbname = %s user = m5221104 password = hagehpge" %(dbname)
    # info = "host = localhost dbname = %s user = postgres" %(dbname)
    conn = psycopg2.connect(info)
    cur = conn.cursor()

    for layer in layers:
        sql = "select observation_id, ST_AsGeoJSON(footprint) , path from %s where ST_DWithin(footprint,ST_GeographyFromText('SRID=4326;POINT(%s %s)'),%s);" %(layer,lon,lat,search_radius)
        cur.execute(sql)
        result = cur.fetchall()
        if not result:
            pass
        else:
            hit_data_list2.append(json_construction(result,str(layer)))

    cur.close()
    field_data = cl.OrderedDict()
    field_data["hit_data"] = hit_data_list2
    json_data = json.dumps(field_data)
    return json_data


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def db(request):
    params_json = json.loads(request.body)
    json_data = db_connect(params_json)
    return HttpResponse(json_data)