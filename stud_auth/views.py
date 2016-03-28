from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView


class UsersListView(ListView):
    model = User
    template_name = 'registration/users_list.html'
    context_object_name = 'users'
    #paginate_by = 10


class UserDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user_info'
