from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate
from .forms import LoginForm, SignupForm, RequestRideForm, RequestShareForm, RegisterVehicleForm, EditOpenRideFormOwner, EditOpenRideFormSharer, EditUserInfoForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Userinfo, Ride
from django.db.models import Q


# Create your views here.

@login_required
def index(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    
    return render(request, 'rideshareapp/index.html', {'userinfo': userinfo})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('rideshareapp:login'))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # check username and password are valid
            user = authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('rideshareapp:index'))
            else:
                error_msg = "User or password is not correct"
                return render(request, 'rideshareapp/login.html', {'form': form, 'error_msg': error_msg})
        else:
            return render(request, 'rideshareapp/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'rideshareapp/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, email=email)
            Userinfo.objects.create(user=user, user_name=user.username, driver_status=False)
            return HttpResponseRedirect(reverse('rideshareapp:login'))
    else:
        form = SignupForm()
    return render(request, 'rideshareapp/signup.html', {'form': form})


@login_required
def request_ride(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    if request.method == 'POST':
        form = RequestRideForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data.get('destination')
            arrival_time = form.cleaned_data.get('arrival_time')
            owner_num = form.cleaned_data.get('owner_num')
            shared_status = form.cleaned_data.get('shared_status')
            vehicle_type = form.cleaned_data.get('vehicle_type')
            special_request = form.cleaned_data.get('special_request')
            Ride.objects.create(user = userinfo, owner_name = userinfo.user_name, destination = destination, arrival_time = arrival_time, owner_num = owner_num, 
                shared_status = shared_status, vehicle_type = vehicle_type, special_request = special_request, passenger_num = owner_num)

            return HttpResponseRedirect(reverse('rideshareapp:index'))
            
    else:
        form = RequestRideForm()
    return render(request, 'rideshareapp/request_ride.html', {'form': form})

@login_required
def edit_vehicle(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    if request.method == 'POST':
        form = RegisterVehicleForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data.get('type')
            plate = form.cleaned_data.get('plate')
            special_vehicle_info =form.cleaned_data.get('special_vehicle_info')
            passengers_num = form.cleaned_data.get('passengers_num')
            userinfo.type = type
            userinfo.plate = plate
            userinfo.special_vehicle_info = special_vehicle_info
            userinfo.passengers_num = passengers_num
            userinfo.driver_status = True
            userinfo.save()
            return HttpResponseRedirect(reverse('rideshareapp:index'))
    else:
        form = RegisterVehicleForm()
        if userinfo.driver_status:
            form.fields["plate"].initial = userinfo.plate
            form.fields["type"].initial = userinfo.type
            form.fields["special_vehicle_info"].initial = userinfo.special_vehicle_info
            form.fields["passengers_num"].initial = userinfo.passengers_num

        
    return render(request, 'rideshareapp/edit_vehicle.html', {'form': form})

@login_required
def find_order(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    type = userinfo.type
    vehicle_capacity = userinfo.passengers_num  
    ride_typ_filled = Ride.objects.filter(ride_status='open', passenger_num__lte = vehicle_capacity, vehicle_type=type)
    ride_typ_null = Ride.objects.filter(ride_status='open', passenger_num__lte = vehicle_capacity, vehicle_type='')
    ride_all = ride_typ_filled|ride_typ_null
    result_ride = []
    for each_ride in list(ride_all):
        if each_ride.owner_name != userinfo.user_name and userinfo.user_name not in each_ride.sharer_name:
            result_ride.append(each_ride)
    return render(request, 'rideshareapp/find_order.html', {'result_ride': result_ride})

@login_required
def take_order(request, ride_id):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    ride = get_object_or_404(Ride, id = ride_id)
    ownerName = ride.owner_name
    sharerName = ride.sharer_name
    email_list = []
    ownerEmail = get_object_or_404(User, username = ownerName).email
    if ownerEmail:
        email_list.append(ownerEmail)
    for sharer in sharerName:
        sharerEmail = get_object_or_404(User, username = sharer).email
        if sharerEmail:
            email_list.append(sharerEmail)
    
    if request.method == 'POST':
        # print(email_list)
        send_mail(
            'RideShare Order Confirmed',
            'Your order is confirmed by a driver',
            'rideshareyz@outlook.com',
            email_list,
            fail_silently=False,
        )
        ride.ride_status = 'confirmed'
        ride.driver_name = userinfo.user_name
        ride.vehicle_type = userinfo.type 
        ride.save()
        
        return HttpResponseRedirect(reverse('rideshareapp:index'))
    return render(request, 'rideshareapp/take_order.html', {'ride': ride})


@login_required
def register_driver(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    if request.method == 'POST':
        form = RegisterVehicleForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data.get('type')
            plate = form.cleaned_data.get('plate')
            special_vehicle_info =form.cleaned_data.get('special_vehicle_info')
            passengers_num = form.cleaned_data.get('passengers_num')
            userinfo.type = type
            userinfo.plate = plate
            userinfo.special_vehicle_info = special_vehicle_info
            userinfo.passengers_num = passengers_num
            userinfo.driver_status = True
            userinfo.save()
            return HttpResponseRedirect(reverse('rideshareapp:index'))
    else:
        form = RegisterVehicleForm()
    return render(request, 'rideshareapp/register_driver.html', {'form': form})
            




@login_required
def request_share(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    if request.method == 'POST':
        form = RequestShareForm(request.POST)
        if form.is_valid():
            arrival_from = form.cleaned_data.get('arrival_from')
            arrival_to = form.cleaned_data.get('arrival_to')
            destination = form.cleaned_data.get('destination')
            sharer_num = form.cleaned_data.get('sharer_num')
            ride_all = Ride.objects.filter(destination = destination, arrival_time__range=[arrival_from, arrival_to], ride_status='open', shared_status = True)
            
            result_ride = []
            for each_ride in list(ride_all):
                if userinfo.user_name not in each_ride.sharer_name and userinfo.user_name != each_ride.owner_name:
                    result_ride.append(each_ride)


            return render(request, 'rideshareapp/find_share.html', {'result_ride': result_ride, 'sharer_num': sharer_num})
            
    else:
        form = RequestShareForm()
    return render(request, 'rideshareapp/request_share.html', {'form': form})


@login_required
def join_share(request, ride_id, sharer_num):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    ride = get_object_or_404(Ride, id = ride_id)
    if request.method == 'POST':
        # update ride
        ride.sharer_num.append([user.id, sharer_num])
        ride.sharer_name.append(userinfo.user_name)
        ride.passenger_num = ride.passenger_num + sharer_num
        ride.save()
        return HttpResponseRedirect(reverse('rideshareapp:index'))
    return render(request, 'rideshareapp/join_share.html', {'ride': ride, 'sharer_num': sharer_num})


@login_required
def find_open(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    sharer_list = []
    sharer_list.append(userinfo.user_name)
    sharer_ride = Ride.objects.filter(ride_status='open', sharer_name__contains=sharer_list)
    owner_ride = Ride.objects.filter(ride_status='open', owner_name = userinfo.user_name)
    return render(request, 'rideshareapp/find_open.html', { 'sharer_ride': sharer_ride, 'owner_ride': owner_ride})


def check_sharer(ride):
    if ride.shared_status == False:
        ride.sharer_num = []
        ride.sharer_name = []
        ride.passenger_num = ride.owner_num



@login_required
def edit_open(request, ride_id):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    ride = get_object_or_404(Ride, id = ride_id)
    
    if request.method == 'POST':
        if userinfo.user_name == ride.owner_name:
            form = EditOpenRideFormOwner(request.POST)
            if form.is_valid():
                destination = form.cleaned_data.get('destination')
                arrival_time = form.cleaned_data.get('arrival_time')
                owner_num =form.cleaned_data.get('owner_num')
                shared_status = form.cleaned_data.get('shared_status')
                vehicle_type = form.cleaned_data.get('vehicle_type')
                special_request = form.cleaned_data.get('special_request')
                ride.destination = destination
                ride.arrival_time = arrival_time
                ride.passenger_num = ride.passenger_num - ride.owner_num
                ride.owner_num = owner_num
                ride.passenger_num = ride.passenger_num + ride.owner_num
                ride.shared_status = shared_status
                ride.vehicle_type = vehicle_type
                ride.special_request = special_request
                check_sharer(ride)
                ride.save()
                return HttpResponseRedirect(reverse('rideshareapp:find_open'))
            else:
                return render(request, 'rideshareapp/edit_open.html', {'form': form, 'ride_id': ride_id})
                
        else:
            form = EditOpenRideFormSharer(request.POST)
            if form.is_valid():   
                sharer_n = form.cleaned_data.get('sharer_num')
                for i in range (len(ride.sharer_num)):
                    if user.id == ride.sharer_num[i][0]:
                        sharer_number = ride.sharer_num[i][1]
                        ride.sharer_num[i][1] = sharer_n
                        ride.passenger_num = ride.passenger_num - sharer_number + sharer_n
                ride.save()
                return HttpResponseRedirect(reverse('rideshareapp:find_open'))
            else:
                return render(request, 'rideshareapp/edit_open.html', {'form': form, 'ride_id': ride_id})
    else:
        if userinfo.user_name == ride.owner_name:
            form = EditOpenRideFormOwner()
            form.fields["destination"].initial = ride.destination
            form.fields["arrival_time"].initial = ride.arrival_time
            form.fields["owner_num"].initial = ride.owner_num
            form.fields["shared_status"].initial = ride.shared_status
            form.fields["vehicle_type"].initial = ride.vehicle_type
            form.fields["special_request"].initial = ride.special_request
        else:
            form = EditOpenRideFormSharer()
            for sharer_id, sharer_number in ride.sharer_num:
                if user.id == sharer_id:
                    form.fields["sharer_num"].initial = sharer_number
            
    return render(request, 'rideshareapp/edit_open.html', {'form': form, 'ride_id': ride_id})


@login_required
def cancel_order(request, ride_id):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    ride = get_object_or_404(Ride, id = ride_id)
    if request.method == 'POST':
        if userinfo.user_name == ride.owner_name:
            ride.delete()
        else:
            for i in range (len(ride.sharer_num)):
                if user.id == ride.sharer_num[i][0]:
                    ride.passenger_num = ride.passenger_num - ride.sharer_num[i][1]       
                    ride.sharer_num.pop(i) 
                    break        
            ride.sharer_name.remove(userinfo.user_name)          
            ride.save()
        return HttpResponseRedirect(reverse('rideshareapp:find_open'))
    return render(request, 'rideshareapp/cancel_order.html')


@login_required
def find_confirmed(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    sharer_list = []
    sharer_list.append(userinfo.user_name)
    sharer_ride = Ride.objects.filter(ride_status='confirmed', sharer_name__contains=sharer_list)
    owner_ride = Ride.objects.filter(ride_status='confirmed', owner_name = userinfo.user_name)

    driver_ride = Ride.objects.filter(ride_status='confirmed', driver_name = userinfo.user_name)
    return render(request, 'rideshareapp/find_confirmed.html', { 'passenger_ride': sharer_ride|owner_ride, 'driver_ride': driver_ride})


@login_required
def super_ride(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    sharer_list = []
    sharer_list.append(userinfo.user_name)
    driver_ride = Ride.objects.filter(~Q(ride_status='complete'), driver_name = userinfo.user_name)
    sharer_ride = Ride.objects.filter(~Q(ride_status='complete'), sharer_name__contains=sharer_list)
    owner_ride = Ride.objects.filter(~Q(ride_status='complete'), owner_name = userinfo.user_name)
    return render(request, 'rideshareapp/super_ride.html', {'driver_ride': driver_ride, 'sharer_ride': sharer_ride, 'owner_ride': owner_ride})


@login_required
def view_ride(request, ride_id):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    ride = get_object_or_404(Ride, id = ride_id)
    driverinfo = None
    if ride.driver_name:
        driverinfo = get_object_or_404(Userinfo, user_name = ride.driver_name)
        return render(request, 'rideshareapp/view_ride.html', {'driverinfo':driverinfo, 'ride':ride})
    else:
        return render(request, 'rideshareapp/view_ride.html', {'driverinfo':driverinfo, 'ride':ride})



@login_required
def finish_ride(request, ride_id):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    ride = get_object_or_404(Ride, id = ride_id)
    ride.ride_status = "complete"
    ride.save()
    return HttpResponseRedirect(reverse('rideshareapp:find_confirmed'))

@login_required
def view_personal(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    return render(request, 'rideshareapp/view_personal.html', {'userinfo': userinfo, 'user': user})

@login_required
def edit_useraccount(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    if request.method == 'POST':
        form = EditUserInfoForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.save()
            return HttpResponseRedirect(reverse('rideshareapp:view_personal'))
        else:
            return render(request, 'rideshareapp/edit_useraccount.html', {'form': form})
    else:
        form = EditUserInfoForm()
        form.fields["firstname"].initial = user.first_name
        form.fields["lastname"].initial = user.last_name
        form.fields["email"].initial = user.email
    return render(request, 'rideshareapp/edit_useraccount.html', {'form': form})


@login_required
def delete_driver(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo, user=user)
    ride = Ride.objects.filter(driver_name = userinfo.user_name, ride_status = 'confirmed')
    
    if request.method == 'POST':
        if ride:
            error_msg = "You can not delete your driver status because you have confirmed ride"
            return render(request, 'rideshareapp/delete_driver.html', {'error_msg': error_msg})
            
        else:
            userinfo.driver_status = False
            userinfo.plate = None
            userinfo.type = None
            userinfo.passengers_num = None
            userinfo.special_vehicle_info = None
            userinfo.save()
            return HttpResponseRedirect(reverse('rideshareapp:index'))
            
    return render(request, 'rideshareapp/delete_driver.html')

