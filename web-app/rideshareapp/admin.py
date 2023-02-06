from django.contrib import admin

from .models import User, Userinfo, Ride

# Register your models here.
admin.site.register(Userinfo)
admin.site.register(Ride)
