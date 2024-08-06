from django.db import models

class SuperCam(models.Model):
    file_name = models.CharField(max_length=255)
    obs_id = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    sol = models.IntegerField()
    csv_wavelength = models.TextField()
    csv_reflectance = models.TextField()

class SuperCamMeta(models.Model):
    file_name = models.CharField(max_length=255)
    product_class = models.TextField()
    title = models.TextField()
    version_id = models.TextField()
    local_mean_solar_time = models.TextField()
    local_true_solar_time = models.TextField()
    processing_level = models.TextField()
    solar_longitude = models.TextField()
    solar_longitude_unit = models.TextField()
    start_date_time = models.TextField()
    stop_date_time = models.TextField()
