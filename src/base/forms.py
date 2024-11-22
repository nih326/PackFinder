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
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['address', 'rent', 'description', 'available_from']
        widgets = {
            'available_from': forms.DateInput(attrs={'type': 'date'})
        }
        
from django import forms
from .models import MatchPreferences

class MatchPreferencesForm(forms.ModelForm):
    class Meta:
        model = MatchPreferences
        exclude = ['profile']
        widgets = {
            'cleanliness': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'noise_level': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'guests_frequency': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'early_bird': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'night_owl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'study_at_home': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'study_quiet_needed': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'smoking_tolerance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pet_friendly': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shared_spaces_comfort': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }
        
from django import forms
from .models import Profile

class RoommatePreferenceForm(forms.ModelForm):
    """Form for updating roommate preferences."""
    class Meta:
        model = Profile
        fields = [
            'sleep_schedule',
            'sleep_schedule_importance',
            'cleanliness',
            'cleanliness_importance',
            'noise_preference',
            'noise_importance',
            'guest_preference',
            'guest_importance',
        ]
        widgets = {
            'sleep_schedule': forms.Select(attrs={'class': 'form-control'}),
            'sleep_schedule_importance': forms.Select(attrs={'class': 'form-control'}),
            'cleanliness': forms.Select(attrs={'class': 'form-control'}),
            'cleanliness_importance': forms.Select(attrs={'class': 'form-control'}),
            'noise_preference': forms.Select(attrs={'class': 'form-control'}),
            'noise_importance': forms.Select(attrs={'class': 'form-control'}),
            'guest_preference': forms.Select(attrs={'class': 'form-control'}),
            'guest_importance': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
# Delay import to avoid circular dependency
MatchPreferences = None

def get_match_preferences_model():
    global MatchPreferences
    if MatchPreferences is None:
        from .models import MatchPreferences
    return MatchPreferences

class MatchPreferencesForm(forms.ModelForm):
    class Meta:
        model = get_match_preferences_model()
        fields = '__all__'
