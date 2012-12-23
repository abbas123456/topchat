from django import forms
from client import models
from django.contrib.auth.models import User
from django.forms.widgets import Select
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from account.views import UserListApiView


class RoomForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea({'rows': '2'}))

    class Meta:
        model = models.Room
        exclude = ('created_by', 'created_date', 'slug', 'appearance')


class AutoCompleteWidget(Select):

    def render(self, name, value, attrs=None, choices=()):
        value = '' if value is None else User.objects.get(id=value)
        return mark_safe(u'<input id="{0}" name="{1}" type="text"'
                         ' value="{2}" autocomplete="off">'.format(attrs['id'],
                                                                   name,
                                                                   value))


class RoomAdministratorForm(forms.ModelForm):

    user_list_queryset = UserListApiView.queryset
    queryset = user_list_queryset.values_list('username', flat=True)
    administrator_choices = [(id, id) for id in queryset]
    administrator = forms.ChoiceField(administrator_choices,
                                      widget=AutoCompleteWidget)

    class Meta:
        model = models.RoomAdministrator
        exclude = ('room')

    def clean_administrator(self):
        try:
            user = User.objects.get(username=self.cleaned_data['administrator'])
            return user
        except:
            raise ValidationError("This user does not exist")
