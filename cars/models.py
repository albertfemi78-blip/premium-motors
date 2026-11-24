from django.db import models
from django.conf import settings
import hashlib
from django.utils import timezone
from datetime import timedelta


class Car(models.Model):

    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Used', 'Used'),
    ]

    TRANSMISSION_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
    ]

    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES
    )

    transmission = models.CharField(
        max_length=10,
        choices=TRANSMISSION_CHOICES
    )

    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_CHOICES
    )

    mileage = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    colour = models.CharField(max_length=50)
    description = models.TextField()

    image = models.ImageField(
        upload_to='cars/',
        blank=True,
        null=True
    )

    is_available = models.BooleanField(default=True)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.manufacturer} {self.name} ({self.year})"


class CarEnquiry(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Contacted', 'Contacted'),
        ('Completed', 'Completed'),
    ]

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    # Connect enquiries to registered customers
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries'
    )

    full_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.car}"


class CarImage(models.Model):

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='cars/')

    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image of {self.car}"
class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return (
            not self.is_used
            and timezone.now() < self.expires_at
            and self.attempts < 5
        )

    def __str__(self):
        return f"Password reset OTP for {self.email}"