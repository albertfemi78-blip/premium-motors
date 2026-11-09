
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/enquire/', views.car_enquiry, name='car_enquiry'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

