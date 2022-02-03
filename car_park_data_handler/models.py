from django.db import models


# Create your models here.

class Carpark(models.Model):
    car_park_id = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    development = models.CharField(
        max_length=100)  # this is the human-readable name of parking lot, but does not exist for all
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    lot_type = models.CharField(max_length=1)
    agency = models.CharField(max_length=3)

    def __str__(self):
        return self.car_park_id


class CarparkData(models.Model):
    carpark_id = models.ForeignKey(Carpark, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()
    available_lots = models.PositiveSmallIntegerField()
    constraints = [
        models.UniqueConstraint(fields=['car_park_id', 'timestamp'], name='unique timestamp and car park ID')
    ]

    def __str__(self):
        return self.car_park_id + " at " + self.timestamp
