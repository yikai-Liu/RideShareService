from django.urls import path

from . import views

app_name = 'rideshareapp'
urlpatterns = [
    path('index', views.index, name= 'index'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('request_ride/', views.request_ride, name = 'request_ride'),
    path('join_share/<int:ride_id>/<int:sharer_num>', views.join_share, name = 'join_share'),
    path('take_order/<int:ride_id>/', views.take_order, name = 'take_order'),
    path('request_share/', views.request_share, name = 'request_share'),
    path('find_order/', views.find_order, name = 'find_order'),
    path('register_driver/', views.register_driver, name = 'register_driver'),
    path('edit_vehicle/', views.edit_vehicle, name = 'edit_vehicle'),
    path('super_ride/', views.super_ride, name = 'super_ride'),
    path('find_open/', views.find_open, name = 'find_open'),
    path('edit_open/<int:ride_id>', views.edit_open, name = 'edit_open'),
    path('cancel_order/<int:ride_id>', views.cancel_order, name = 'cancel_order'),
    path('find_confirmed/', views.find_confirmed, name = 'find_confirmed'),
    path('view_ride/<int:ride_id>', views.view_ride, name = 'view_ride'),
    path('finish_ride/<int:ride_id>', views.finish_ride, name = 'finish_ride'),
    path('view_personal/', views.view_personal, name = 'view_personal'),
    path('edit_useraccount/', views.edit_useraccount, name = 'edit_useraccount'),
    
]