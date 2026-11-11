import os
import resend

from django.shortcuts import render, get_object_or_404


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

            # Send business notification using Resend
            notification_sent = False

            try:
                resend.api_key = os.getenv('RESEND_API_KEY')

                if not resend.api_key:
                    raise ValueError("RESEND_API_KEY is not configured.")

                business_subject = (
                    f"New Car Enquiry - {car.manufacturer} {car.name}"
                )

                business_message = f"""
                <h2>New Car Enquiry - Premium Motors</h2>

                <h3>Customer Details</h3>
                <p><strong>Name:</strong> {enquiry.full_name}</p>
                <p><strong>Email:</strong> {enquiry.email}</p>
                <p><strong>Phone:</strong> {enquiry.phone}</p>

                <h3>Car Details</h3>
                <p><strong>Car:</strong> {car.year} {car.manufacturer} {car.name}</p>
                <p><strong>Price:</strong> NGN {car.price:,.2f}</p>

                <h3>Customer Message</h3>
                <p>{enquiry.message}</p>

                <p>Please contact this customer as soon as possible.</p>

                <p>Premium Motors Website Notification</p>
                """

                resend.Emails.send({
                    "from": "Premium Motors <onboarding@resend.dev>",
                    "to": [os.getenv('RESEND_TO_EMAIL')],
                    "subject": business_subject,
                    "html": business_message
                })

                notification_sent = True

                print("Business notification sent successfully.")

            except Exception as error:
                print("Resend notification failed:", error)

            # Display enquiry success page
            return render(
                request,
                'cars/enquiry_success.html',
                {
                    'car': car,
                    'email_sent': False,
                    'notification_sent': notification_sent
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