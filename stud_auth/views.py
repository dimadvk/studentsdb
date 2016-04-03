from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

from .models import StProfile
from .forms import ProfileEditForm

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
#    def render_to_response(self, context, **response_kwargs):
#        import ipdb; ipdb.set_trace()
#        return super(UserDetailView, self).render_to_response(self, context, **response_kwargs)

def test(request):
    # text = reverse('registration_activate', activation_key='60f3d1426a1e99a9a6387945f17b2d77038ba165')
    # 60f3d1426a1e99a9a6387945f17b2d77038ba165
    # text = reverse('registration_complete')
    return HttpResponse('-')

class UserUpdateView(SuccessMessageMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = 'registration/profile_edit.html'
    success_message = _(u'Profile successfully updated!')
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        obj, created = StProfile.objects.get_or_create(user=self.request.user)
        return obj

