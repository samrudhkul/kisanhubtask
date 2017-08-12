from django.db import models

# Create your models here.
class Weatherdata(models.Model):
    unique_string= models.CharField(max_length=200,primary_key=True)
    weather_country = models.CharField(max_length=200)
    weather_type = models.CharField(max_length=200)
    weather_year = models.IntegerField(default=0)
    month_or_season=models.CharField(max_length=200)
    weather_reading=models.FloatField(default=0)