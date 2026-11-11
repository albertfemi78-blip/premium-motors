from django.contrib import admin
from .models import Car, CarEnquiry, CarImage

class CarImageInline(admin.TabularInline):
model = CarImage
extra = 1
fields = ('image',)
verbose_name = "Car Image"
verbose_name_plural = "Additional Car Images"

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
list_display = (
'name',
'manufacturer',
'year',
'price',
'condition',
'transmission',
'fuel_type',
'is_available',
)


list_filter = (
    'condition',
    'transmission',
    'fuel_type',
    'is_available',
)

search_fields = ('name', 'manufacturer')
list_per_page = 20
ordering = ('-date_added',)

inlines = [CarImageInline]


@admin.register(CarEnquiry)
class CarEnquiryAdmin(admin.ModelAdmin):
list_display = (
'full_name',
'car',
'email',
'phone',
'date_submitted',
)


search_fields = ('full_name', 'email', 'car__name')
list_filter = ('date_submitted',)
list_per_page = 20
ordering = ('-date_submitted',)

readonly_fields = ('date_submitted',)

