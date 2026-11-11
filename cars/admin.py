from django.contrib import admin
from django.utils.html import format_html

from .models import Car, CarEnquiry, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" width="120" height="80" '
                'style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image uploaded"

    image_preview.short_description = "Image Preview"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'manufacturer',
        'year',
        'price',
        'condition',
        'is_available',
        'main_image_preview',
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

    readonly_fields = ('main_image_preview',)

    def main_image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" width="120" height="80" '
                'style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No main image"

    main_image_preview.short_description = "Main Image"


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