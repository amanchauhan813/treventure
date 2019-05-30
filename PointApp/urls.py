from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as api_views
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'catalog/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'catalog/logged_out.html'}, name='logout'),
    url(r'^$', views.index, name='index'),
      url(r'^signup/', views.signup, name='signup'),
    url(r'^search/',views.search_results, name = 'search_results'),
    url(r'^bus-details/(\d+)',views.bus_details, name = 'bus_details'),
    url(r'^mobile_payment/(\d+)',views.mobile_payment, name = 'mobile_payment'),
    url(r'^searchtraval/', views.searchtravals, name='searchtraval'),
     url(r'^searchhotel/', views.searchhotels, name='searchhotel'),
    url(r'^search_hotel_results/',views.search_hotel_results, name = 'search_hotel_results'),
     url(r'^room_details/(\d+)/([-\w]+)/([-\w]+)',views.room_details, name = 'room_details'),  
     url(r'^room_booked/',views.room_booked, name = 'room_booked'),   
    url(r'^contact/', views.contact, name='contact'),
    url(r'^flights/', views.flights, name='flights'),
    url(r'^holidays/', views.holidays, name='holidays'),
     url(r'^error/', views.errors, name='error'),    
     url(r'^allbus/', views.allbuss, name='allbus'),
]