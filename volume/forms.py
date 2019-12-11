from django import forms
from .models import Rep, Session
from accounts.models import User


class RepAddForm(forms.ModelForm):

    class Meta:
        model = Rep
        fields = ['session', 'exercice', 'repition', 'weight']

    def __init__(self, user, *args, **kwargs):
        super(RepAddForm, self).__init__(*args, **kwargs)
        self.fields['session'].queryset = Session.objects.filter(user=user)


class SessionForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(SessionForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].initial = self.user

    class Meta:
        model = Session
        fields = ['date', 'body_weight']

    # def clean_user(self):
    #     user = self.instance.user
    #     return user
