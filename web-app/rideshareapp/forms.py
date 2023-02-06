from django import forms
from django.contrib.auth.models import User
from .models import Ride
from django.core.validators import MinValueValidator
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     username = User.objects.filter(username=username)

    #     if not username:
    #         raise forms.ValidationError("Username does not exist!")
    #     return username
        
    # def clean_password(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username = username, password = password)

    #     if not user:
    #         raise forms.ValidationError("Password does not match!")
    #     return password

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    firstname = forms.CharField(label='First name', max_length=100, required=False)
    lastname = forms.CharField(label='Last name', max_length=100, required=False)
    email = forms.EmailField(label='Email Address', required=False)

class EditUserInfoForm(forms.Form):
    firstname = forms.CharField(label='First name', max_length=100, required=False)
    lastname = forms.CharField(label='Last name', max_length=100, required=False)
    email = forms.EmailField(label='Email Address', required=False)

class RequestRideForm(forms.Form):
    destination = forms.CharField(label='destination', max_length=100)
    arrival_time = forms.DateTimeField(label='Arrival Time')
    owner_num = forms.IntegerField(label='Number of passengers')
    shared_status = forms.BooleanField(label='Shared or Not', required=False)
    vehicle_type = forms.CharField(label='Vehicle Type', max_length=100, required=False)
    special_request = forms.CharField(label='Special Request', max_length=100, required=False)

class RequestShareForm(forms.Form):
    arrival_from = forms.DateTimeField(label='Arrival Time From')
    arrival_to = forms.DateTimeField(label='Arrival Time To')
    destination = forms.CharField(label='Destination address', max_length=100)
    sharer_num = forms.IntegerField(label='Number of sharers')

class RegisterVehicleForm(forms.Form):
    plate = forms.CharField(label='plate', max_length=100)
    type = forms.CharField(label='type', max_length=100)
    special_vehicle_info = forms.CharField(label='special_vehicle_info', max_length=100, required=False)
    passengers_num = forms.IntegerField(label='passengers_num')

class EditOpenRideFormOwner(forms.Form):
    destination = forms.CharField(label='destination', max_length=100)
    arrival_time = forms.DateTimeField(label='Arrival Time')
    owner_num = forms.IntegerField(label='Number of passengers')
    shared_status = forms.BooleanField(label='Shared or Not', required=False)
    vehicle_type = forms.CharField(label='Vehicle Type', max_length=100, required=False)
    special_request = forms.CharField(label='Special Request', max_length=100, required=False)

    def clean_owner_num(self):
        owner_num = self.cleaned_data.get('owner_num')

        if owner_num <= 0:
            raise forms.ValidationError("You can not set non-positive owner number!")
        return owner_num

class EditOpenRideFormSharer(forms.Form):
    sharer_num = forms.IntegerField(label='Number of sharers', validators=[MinValueValidator(1)])

    def clean_sharer_num(self):
        sharer_num = self.cleaned_data.get('sharer_num')

        if sharer_num <= 0:
            raise forms.ValidationError("You can not set non-positive sharer number!")
        return sharer_num