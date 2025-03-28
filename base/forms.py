# forms.py
from django import forms
from .models import UserFeedback

# forms.py

from .models import Notification


class ClubAdminLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']



class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['feedback_text']