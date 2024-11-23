#
# Created on Sun Oct 04 2024
#
# The MIT License (MIT)
# Copyright (c) 2024 Chaitralee Datar, Ananya Patankar, Yash Shah
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .utils import check_ncsu_email

# from django.contrib.admin.widgets import AdminDateWidget
from .models import Profile, Room


class SignUpForm(UserCreationForm):
    """Build Sign up Form"""

    # username = forms.CharField(label="<b>NCSU</b> E-mail", max_length=100)
    class Meta:
        model = get_user_model()
        fields = [
            "email",
        ]

    def clean(self):
        # data is feteched using the super function of django
        super(SignUpForm, self).clean()

        email = self.cleaned_data.get("email")

        if not check_ncsu_email(email):
            self._errors["email"] = self.error_class(
                ["Please use a valid ncsu email id"]
            )

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    """Build the User Profile Form"""

    # birth_date = forms.DateField(widget=AdminDateWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['sleep_schedule'].widget.attrs.update({'class': 'form-control'})
        self.fields['sleep_schedule_importance'].widget.attrs.update({'class': 'form-control'})
        self.fields['cleanliness'].widget.attrs.update({'class': 'form-control'})
        self.fields['cleanliness_importance'].widget.attrs.update({'class': 'form-control'})
        self.fields['noise_preference'].widget.attrs.update({'class': 'form-control'})
        self.fields['noise_importance'].widget.attrs.update({'class': 'form-control'})
        self.fields['guest_preference'].widget.attrs.update({'class': 'form-control'})
        self.fields['guest_importance'].widget.attrs.update({'class': 'form-control'})
        self.fields['room_status'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['diet'].widget.attrs.update({'class': 'form-control'})
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['degree'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender_preference'].widget.attrs.update({'class': 'form-control'})
        self.fields['diet_preference'].widget.attrs.update({'class': 'form-control'})
        self.fields['course_preference'].widget.attrs.update({'class': 'form-control'})
        self.fields['degree_preference'].widget.attrs.update({'class': 'form-control'})
        self.fields['country_preference'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = [
            'name',
            'profile_photo',
            'bio',
            'sleep_schedule',
            'sleep_schedule_importance',
            'cleanliness',
            'cleanliness_importance',
            'noise_preference',
            'noise_importance',
            'guest_preference',
            'guest_importance',
            'room_status',
            'gender',
            'degree',
            'diet',
            'course',
            'country',
            'gender_preference',
            'degree_preference',
            'diet_preference',
            'course_preference',
            'country_preference',
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['address', 'rent', 'description', 'available_from']
        widgets = {
            'available_from': forms.DateInput(attrs={'type': 'date'})
        }
