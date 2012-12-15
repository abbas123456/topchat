from django import forms
from client import models


class RoomForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea({'rows': '2'}))

    class Meta:
        model = models.Room
        exclude=('created_by', 'created_date', 'slug')
