import os
import resend
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Car, CarEnquiry
from .forms import CarEnquiryForm, UserRegisterForm
import random
import hashlib
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import PasswordResetOTP


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

            # Connect enquiry to customer if logged in
            if request.user.is_authenticated:
                enquiry.user = request.user

            enquiry.save()

            # Send business notification using Resend
            notification_sent = False

            try:
                resend.api_key = os.getenv('RESEND_API_KEY')

                if not resend.api_key:
                    raise ValueError(
                        "RESEND_API_KEY is not configured."
                    )

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
                <p><strong>Car:</strong>
                {car.year} {car.manufacturer} {car.name}</p>

                <p><strong>Price:</strong> NGN {car.price:,.2f}</p>

                <h3>Customer Message</h3>
                <p>{enquiry.message}</p>

                <p>Please contact this customer as soon as possible.</p>

                <p>Premium Motors Website Notification</p>
                """

                recipient_email = os.getenv('RESEND_TO_EMAIL', '').strip()

                if not recipient_email:
                    raise ValueError("RESEND_TO_EMAIL is not configured.")

                resend.Emails.send({
                    "from": "Premium Motors <onboarding@resend.dev>",
                    "to": [recipient_email],
                    "subject": business_subject,
                    "html": business_message
                })

                notification_sent = True

                print("Business notification sent successfully.")

            except Exception as error:
                print("Resend notification failed:", error)

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


# Customer registration
def register(request):

    if request.user.is_authenticated:
        return redirect('customer_dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']

            # Prevent duplicate email addresses
            if User.objects.filter(email__iexact=email).exists():
                form.add_error(
                    'email',
                    'An account with this email already exists.'
                )

            else:
                user = form.save()

                # Automatically log in after registration
                login(request, user)

                messages.success(
                    request,
                    'Your Premium Motors account was created successfully!'
                )

                return redirect('customer_dashboard')

    else:
        form = UserRegisterForm()

    return render(request, 'cars/register.html', {
        'form': form
    })


# Customer logout
@login_required
@require_POST
def customer_logout(request):
    logout(request)

    messages.success(
        request,
        'You have successfully logged out.'
    )

    return redirect('home')


# Customer dashboard
@login_required
def customer_dashboard(request):

    enquiries = CarEnquiry.objects.filter(
        user=request.user
    ).select_related('car').order_by('-date_submitted')

    total_enquiries = enquiries.count()

    pending_enquiries = enquiries.filter(
        status='Pending'
    ).count()

    reviewed_enquiries = enquiries.filter(
        status='Reviewed'
    ).count()

    return render(
        request,
        'cars/customer_dashboard.html',
        {
            'enquiries': enquiries,
            'total_enquiries': total_enquiries,
            'pending_enquiries': pending_enquiries,
            'reviewed_enquiries': reviewed_enquiries,
        }
    )


# About page
def about(request):
    return render(request, 'cars/about.html')


# Contact page
def contact(request):
    return render(request, 'cars/contact.html')


def forgot_password(request):

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        user = User.objects.filter(
            email__iexact=email,
            is_active=True
        ).first()

        # Always show the same response to avoid revealing accounts.
        if user:
            otp = str(random.SystemRandom().randint(100000, 999999))

            otp_hash = hashlib.sha256(otp.encode()).hexdigest()

            PasswordResetOTP.objects.filter(
                email__iexact=email,
                is_used=False
            ).update(is_used=True)

            PasswordResetOTP.objects.create(
                email=user.email,
                otp_hash=otp_hash,
                expires_at=timezone.now() + timedelta(minutes=5)
            )

            try:
                send_mail(
                    subject='Premium Motors - Password Reset OTP',
                    message=(
                        f'Your password reset OTP is: {otp}\n\n'
                        'This code expires in 5 minutes. '
                        'If you did not request this, ignore this email.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception:
                messages.error(
                    request,
                    'We could not send the OTP. Please try again later.'
                )
                return redirect('forgot_password')

        messages.success(
            request,
            'If an account exists with that email, an OTP has been sent.'
        )
        request.session['reset_email'] = email
        return redirect('verify_otp')
       

    return render(request, 'cars/forgot_password.html')
def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp = request.POST.get('otp', '').strip()

        if not email:
            messages.error(request, 'Please request a new OTP.')
            return redirect('forgot_password')

        record = PasswordResetOTP.objects.filter(
            email__iexact=email,
            is_used=False
        ).order_by('-created_at').first()

        if not record or not record.is_valid():
            messages.error(
                request,
                'OTP has expired. Please request another.'
            )
            return redirect('forgot_password')

        if not otp.isdigit() or len(otp) != 6:
            messages.error(request, 'Enter a valid 6-digit OTP.')
            return redirect('verify_otp')

        record.attempts += 1
        record.save(update_fields=['attempts'])

        otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        if record.otp_hash != otp_hash:
            messages.error(request, 'Incorrect OTP. Please try again.')
            return redirect('verify_otp')

        record.is_used = True
        record.save(update_fields=['is_used'])

        request.session['reset_verified_email'] = email

        return redirect('reset_new_password')

    # This handles GET requests.
    return render(request, 'cars/verify_otp.html')

    email = request.session.get('reset_email')

    if not email:
        messages.error(request, 'Please enter your email first.')
        return redirect('forgot_password')

    if request.method == 'POST':
        otp_input = request.POST.get('otp', '').strip()

        otp_hash_input = hashlib.sha256(otp_input.encode()).hexdigest()

        otp_record = PasswordResetOTP.objects.filter(
            email__iexact=email,
            is_used=False
        ).order_by('-created_at').first()

        if not otp_record:
            messages.error(request, 'No valid OTP found. Please request a new one.')
            return redirect('forgot_password')

        if not otp_record.is_valid():
            messages.error(request, 'The OTP has expired or is no longer valid.')
            return redirect('forgot_password')

        if otp_record.otp_hash != otp_hash_input:
            otp_record.attempts += 1
            otp_record.save()
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')

        # Mark the OTP as used
        otp_record.is_used = True
        otp_record.save()

        # Store the verified email in session for password reset
        request.session['reset_verified_email'] = email

        messages.success(request, 'OTP verified successfully. You can now reset your password.')
        return redirect('reset_new_password')


        return render(request, 'cars/verify_otp.html')
def reset_new_password(request):
    email = request.session.get('reset_verified_email')

    if not email:
        messages.error(request, 'Please verify your OTP first.')
        return redirect('forgot_password')

    user = User.objects.filter(
        email__iexact=email,
        is_active=True
    ).first()

    if not user:
        messages.error(request, 'Account not found.')
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        else:
            try:
                validate_password(password, user)

                user.set_password(password)
                user.save()

                request.session.pop('reset_email', None)
                request.session.pop('reset_verified_email', None)

                messages.success(
                    request,
                    'Your password has been changed successfully. Please log in.'
                )

                return redirect('login')

            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)

    return render(request, 'cars/reset_new_password.html')