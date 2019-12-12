from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from .models import User
from .forms import UserSignUpForm
# Create your views here.


class UserSignUpForm(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
