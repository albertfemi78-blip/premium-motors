from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),

    # Cars
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/enquire/', views.car_enquiry, name='car_enquiry'),

    # Customer authentication
    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='cars/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path('logout/', views.customer_logout, name='logout'),

    # Customer dashboard
    path(
        'dashboard/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),

    # Other pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

# Password Reset

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='cars/password_reset.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done')
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='cars/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='cars/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='cars/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
    'forgot-password/',
    views.forgot_password,
    name='forgot_password'
),
path(
    'verify-otp/',
    views.verify_otp,
    name='verify_otp'
),
path(
    'reset-new-password/',
    views.reset_new_password,
    name='reset_new_password'
),
path(
    'admin-recovery/',
    views.recover_admin,
    name='admin_recovery'
),
]