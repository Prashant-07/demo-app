from django import forms
from .models import Gender

class UserForm(forms.Form):
    name        = forms.CharField(max_length=100,min_length=3)
    email       = forms.EmailField()
    contact     = forms.CharField(max_length=10,min_length=10)
    gender      = forms.CharField(max_length=6,min_length=1)
    password    = forms.CharField(min_length=8)

    def clean_gender(self):
        gender = ''
        if self.cleaned_data['gender']:
            gender = self.cleaned_data['gender'].lower()

        if gender == 'f' or gender == 'female' or gender == str(Gender.FEMALE):
            self.cleaned_data['gender'] = Gender.FEMALE
        elif gender == 'm' or gender == 'male' or gender == str(Gender.MALE):
            self.cleaned_data['gender'] = Gender.MALE  
        else:
            self.cleaned_data['gender'] = Gender.OTHER
        return self.cleaned_data['gender']

    def clean_contact(self):
        if self.cleaned_data['contact'] and not self.cleaned_data['contact'].isnumeric():
            raise forms.ValidationError("Invalid Contact number, please use 10 digit mobile number");
        return self.cleaned_data['contact']
