from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from .settings import MEDIA_ROOT, DEBUG

from students.views.students import StudentUpdateView, StudentDeleteView, StudentList
from students.views.students import students_ajax_next_page
from students.views.students import students_delete_bunch
from students.views.students_add import students_add
from students.views.custom_contact_form import CustomContactFormView
from students.views.contact_admin import ContactAdminView
from students.views.groups import groups_list
from students.views.groups import GroupDeleteView
from students.views.groups import GroupUpdateView
from students.views.groups import GroupCreateView
from students.views.journal import JournalView
from students.views.action_journal import ActionListView
from stud_auth.views import UsersListView, UserDetailView, UserUpdateView
from registration.backends.default import views as registration_views

#test
from stud_auth.views import test

# need for i18n pattern
js_info_dict = {
    'packages': ('students',),
    'domain': 'djangojs',
}

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$',
        permission_required('students.add_student')(students_add), name='students_add'),
#    url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.students.students_edit', name='students_edit'),
#    url(r'^students/(?P<pk>\d+)/delete/$', 'students.views.students.students_delete', name='students_delete'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        permission_required('students.change_student')(StudentUpdateView.as_view()), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$',
        permission_required('students.delete_student')(StudentDeleteView.as_view()),
        name='students_delete'),
    url(r'^student_list/$', StudentList.as_view(), name='student_list'),

    # trying ajax
    url(r'students/next_page$',
        students_ajax_next_page, name='students_ajax_next_page'),

    # delete bunch of students
    url(r'^students/delete-bunch/$', permission_required('students.delete_student')(students_delete_bunch), name="students_delete_bunch"),


    #Groups urls
    url(r'^groups/$', groups_list, name='groups'),
#    url(r'^groups/add/$',
#        'students.views.groups.groups_add', name='groups_add'),
    url(r'^groups/add/$', permission_required('students.add_group')(GroupCreateView.as_view()), name="groups_add"),
#    url(r'^groups/(?P<pk>\d+)/edit/$',
#        'students.views.groups.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/edit/$',
        permission_required('students.change_group')(GroupUpdateView.as_view()), name="group_edit"),
    url(r'^groups/(?P<pk>\d+)/delete/$',
        login_required(permission_required('students.delete_group', raise_exception=True)(GroupDeleteView.as_view())),
        name='group_delete'),

    # Journal url
    #url(r'^journal/$', 'students.views.journal.journal_list', name='journal'),
    #url(r'^journal/$', JournalView.as_view(), name='journal'),
    url(r'^journal/(?P<pk>\d+)?/?$', login_required(JournalView.as_view()), name='journal'),

    # Admin page
    url(r'^admin/', include(admin.site.urls)),

    # favicon.ico
#    url(r'^/favicon\.ico/$', RedirectView.as_view(url='/static/img/favicon.ico')),


    # Contact Admin Form
    url(r'^contact-admin/$', login_required(ContactAdminView.as_view()),
        name='contact_admin'),
    # contact admin with application django-contact-form
    #url(r'^contact-form/$', include('contact_form.urls')),
    url(r'^contact-form/$',
        CustomContactFormView.as_view(), name='contact_form'),

    # Action List
    url(r'^action-journal/$', login_required(ActionListView.as_view()), name='action_journal'),

    # i18n
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),
    # set_language view
    url('^set-language/$', 'students.views.set_language.set_language', name='set_language'),

    # User related urls
    url(r'^users/profiles/$', login_required(UsersListView.as_view()), name='users_list'),
    url(r'^users/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),
    #url(r'^users/profile/(?P<username>[a-zA-Z@+-_.0-9]+)/$', login_required(UserDetailView.as_view()), name='user_profile'),
    url(r'^users/profile/(?P<pk>\d+)/$', login_required(UserDetailView.as_view()), name='user_profile'),
    url(r'^users/profile/edit/$', login_required(UserUpdateView.as_view()), name='user_profile_edit'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^users/register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/activate/complete/$',
            TemplateView.as_view(template_name='registration/activation_complete.html'),
            name='registration_activation_complete'),
    url(r'^users/password_reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^users/register/$', registration_views.RegistrationView.as_view(), name='registration_register'),
    url(r'^users/activate/(?P<activation_key>\w+)/$', registration_views.ActivationView.as_view(), name='registration_activate'),
    url(r'^users/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^users/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^users/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^users/password_change/$', auth_views.password_change, name='password_change'),
    url(r'^users/password_change/done/$', RedirectView.as_view(pattern_name='profile'), name='password_change_done'),
    url(r'^users/', include('registration.backends.default.urls', namespace='users')),

    # Social Auth Related urls
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),

    #test
    url(r'^test/$', test, name='test'),
    url(r'^test/', include('stud_auth.urls', namespace='test_stud_auth')),
)

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT})
    )

    # for debug_toolbar
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
