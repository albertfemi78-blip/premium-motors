from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from .models import Car
from .forms import CarEnquiryForm


# Homepage
def home(request):
    cars = Car.objects.filter(
        is_available=True
    ).order_by('-date_added')[:3]

    return render(request, 'cars/home.html', {
        'cars': cars
    })


# Display all available cars
def car_list(request):
    cars = Car.objects.filter(is_available=True)

    return render(request, 'cars/car_list.html', {
        'cars': cars
    })


# Display details of one car
def car_detail(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        is_available=True
    )

    return render(request, 'cars/car_detail.html', {
        'car': car
    })


# Handle car enquiries
def car_enquiry(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        is_available=True
    )

    if request.method == 'POST':
        form = CarEnquiryForm(request.POST)

        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.save()

            # Customer confirmation email
            customer_subject = (
                f"Your Enquiry About {car.manufacturer} {car.name}"
            )

            customer_message = f"""
Hello {enquiry.full_name},

Thank you for contacting Premium Motors!

We have successfully received your enquiry about:

Car: {car.year} {car.manufacturer} {car.name}
Price: NGN {car.price:,.2f}

Your enquiry details:
{enquiry.message}

Our team appreciates your interest in this vehicle.
We will review your enquiry and get back to you as soon as possible.

Thank you for choosing Premium Motors.

Best regards,
Premium Motors Team
"""

            email_sent = False

            try:
                send_mail(
                    customer_subject,
                    customer_message,
                    None,
                    [enquiry.email],
                    fail_silently=False
                )

                email_sent = True

            except Exception as error:
                print("Customer email failed:", error)

            # Premium Motors business notification
            business_subject = (
                f"New Car Enquiry - {car.manufacturer} {car.name}"
            )

            business_message = f"""
Hello Premium Motors,

A new car enquiry has been submitted through your website.

CUSTOMER DETAILS

Name: {enquiry.full_name}
Email: {enquiry.email}
Phone: {enquiry.phone}

CAR DETAILS

Car: {car.year} {car.manufacturer} {car.name}
Price: NGN {car.price:,.2f}

CUSTOMER MESSAGE

{enquiry.message}

Please contact this customer as soon as possible.

Premium Motors
Website Enquiry Notification
"""

            try:
                send_mail(
                    business_subject,
                    business_message,
                    None,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False
                )

                print("Business notification sent successfully.")

            except Exception as error:
                print("Business notification failed:", error)

            # Display enquiry success page
            return render(
                request,
                'cars/enquiry_success.html',
                {
                    'car': car,
                    'email_sent': email_sent
                }
            )

    else:
        form = CarEnquiryForm()

    return render(
        request,
        'cars/car_enquiry.html',
        {
            'form': form,
            'car': car
        }
    )


# About page
def about(request):
    return render(request, 'cars/about.html')


# Contact page
def contact(request):
    return render(request, 'cars/contact.html')