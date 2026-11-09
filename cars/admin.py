from django.contrib import admin
from .models import Car, CarEnquiry, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'year', 'price', 'condition', 'is_available')
    list_filter = ('condition', 'transmission', 'fuel_type', 'is_available')
    search_fields = ('name', 'manufacturer')
    inlines = [CarImageInline]


@admin.register(CarEnquiry)
class CarEnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'car', 'email', 'phone', 'date_submitted')
    search_fields = ('full_name', 'email', 'car__name')
    list_filter = ('date_submitted',)