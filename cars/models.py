from django.db import models

# Create your models here.



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

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    full_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    message = models.TextField()

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