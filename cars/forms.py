from django import forms
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