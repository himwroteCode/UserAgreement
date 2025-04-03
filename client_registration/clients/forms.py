# from django import forms
# from .models import Client

# class ClientForm(forms.ModelForm):
#     aadhar_image = forms.ImageField(required=True)
#     pan_image = forms.ImageField(required=True)

#     class Meta:
#         model = Client
#         fields = '__all__'
#         exclude = ['client_id']

from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    aadhar_image = forms.ImageField(required=True)
    pan_image = forms.ImageField(required=True)

    class Meta:
        model = Client
        fields = [
            "client_name", "dob", "gender", "marital_status", "phone_number", 
            "email", "country", "state", "city", "location", 
            "postal_address", "national_id"
        ]

        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
        }
