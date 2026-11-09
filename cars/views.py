
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

            return render(request, 'cars/enquiry_success.html', {
                'car': car
            })

    else:
        form = CarEnquiryForm()

    return render(request, 'cars/car_enquiry.html', {
        'form': form,
        'car': car
    })


# About page
def about(request):
    return render(request, 'cars/about.html')


# Contact page
def contact(request):
    return render(request, 'cars/contact.html')

