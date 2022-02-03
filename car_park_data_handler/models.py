from django.db import models


# Create your models here.

class Carpark(models.Model):
    car_park_id = models.CharField(max_length=10, primary_key=True)
    area = models.CharField(max_length=50)
    development = models.CharField(
        max_length=50)  # this is the human-readable name of parking lot, but does not exist for all
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    lot_type = models.CharField(max_length=1)
    agency = models.CharField(max_length=3)

    def __str__(self):
        return self.car_park_id


class Measurement(models.Model):
    car_park_id = models.ForeignKey(Carpark, on_delete=models.DO_NOTHING, primary_key=True)
    timestamp = models.DateTimeField(primary_key=True)
    available_lots = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.car_park_id + " at " + self.timestamp
