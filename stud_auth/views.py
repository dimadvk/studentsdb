from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from django.http import HttpResponse
from django.core.urlresolvers import reverse


class UsersListView(ListView):
    model = User
    template_name = 'registration/users_list.html'
    context_object_name = 'users'
    #paginate_by = 10


class UserDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user_info'

#    def get_context_data(self, *args, **kwargs):
#        import ipdb; ipdb.set_trace()
#        return super(UserDetailView, self).get_context_data(*args, **kwargs)


def test(request):
    # text = reverse('registration_activate', activation_key='60f3d1426a1e99a9a6387945f17b2d77038ba165')
    # 60f3d1426a1e99a9a6387945f17b2d77038ba165
    # text = reverse('registration_complete')
    text = reverse('test_stud_auth:test_inner', args=['arg1'])
    return HttpResponse(text)
