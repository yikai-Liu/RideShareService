from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Userinfo(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_name = models.CharField(max_length=200)
    driver_status = models.BooleanField()
    type = models.CharField(max_length=200, null=True)
    plate = models.CharField(max_length=200, null=True)
    passengers_num = models.IntegerField(null=True)
    special_vehicle_info = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user_name

class Ride(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    arrival_time = models.DateTimeField('Arrival date & time')
    shared_status = models.BooleanField(default=False)
    owner_num = models.IntegerField()
    passenger_num = models.IntegerField()

    sharer_num = ArrayField(ArrayField(models.IntegerField()), default=[])
    sharer_name = ArrayField(models.CharField(max_length=200), default=[])
    
    ride_status = models.CharField(max_length=200, default='open')
    driver_name = models.CharField(max_length=200, null=True, blank=True)
    vehicle_type = models.CharField(max_length=200, blank=True)
    special_request = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.owner_name
