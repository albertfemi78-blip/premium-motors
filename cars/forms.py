from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CarEnquiry


class CarEnquiryForm(forms.ModelForm):

    class Meta:
        model = CarEnquiry

        fields = [
            'full_name',
            'email',
            'phone',
            'message',
        ]

        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your enquiry here...'
            }),
        }


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    first_name = forms.CharField(
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        max_length=150,
        required=True
    )
    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]