from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from .settings import MEDIA_ROOT, DEBUG

from students.views.students import StudentUpdateView, StudentDeleteView, StudentList
from students.views.students import students_ajax_next_page
from students.views.students import students_delete_bunch
from students.views.custom_contact_form import CustomContactFormView
from students.views.contact_admin import ContactAdminView
from students.views.groups import GroupDeleteView
from students.views.groups import GroupUpdateView
from students.views.groups import GroupCreateView
from students.views.journal import JournalView
from students.views.action_journal import ActionListView

#test
from django.views.generic import RedirectView

# need for i18n pattern
js_info_dict = {
    'packages': ('students',),
    'domain': 'djangojs',
}

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$',
        'students.views.students_add.students_add', name='students_add'),
#    url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.students.students_edit', name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', 'students.views.students.students_delete', name='students_delete'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        StudentUpdateView.as_view(), name='students_edit'),
#    url(r'^students/(?P<pk>\d+)/delete/$',
#        StudentDeleteView.as_view(),
#        name='students_delete'),
    url(r'^student_list/$', StudentList.as_view()),

    # trying ajax
    url(r'students/next_page$',
        students_ajax_next_page, name='students_ajax_next_page'),
    #test templateView
    url('^test/$', RedirectView.as_view(pattern_name="home")),

    # delete bunch of students
    url(r'^students/delete-bunch/$', students_delete_bunch, name="students-delete-bunch"),


    #Groups urls
    url(r'^groups/$',
        'students.views.groups.groups_list', name='groups'),
#    url(r'^groups/add/$',
#        'students.views.groups.groups_add', name='groups_add'),
    url(r'^groups/add/$', GroupCreateView.as_view(), name="groups_add"),
#    url(r'^groups/(?P<pk>\d+)/edit/$',
#        'students.views.groups.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/edit/$',
        GroupUpdateView.as_view(), name="group_edit"),
    url(r'^groups/(?P<pk>\d+)/delete/$', 
        GroupDeleteView.as_view(), name='group_delete'),

    # Journal url
    #url(r'^journal/$', 'students.views.journal.journal_list', name='journal'),
    #url(r'^journal/$', JournalView.as_view(), name='journal'),
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    # Admin page
    url(r'^admin/', include(admin.site.urls)),

    # favicon.ico
#    url(r'^/favicon\.ico/$', RedirectView.as_view(url='/static/img/favicon.ico')),


    # Contact Admin Form
    url(r'^contact-admin/$', ContactAdminView.as_view(),
        name='contact_admin'),
    # contact admin with application django-contact-form
    #url(r'^contact-form/$', include('contact_form.urls')),
    url(r'^contact-form/$',
        CustomContactFormView.as_view(), name='contact_form'),

    # Action List
    url(r'^action-journal/$', ActionListView.as_view(), name='action_journal'),

    # i18n
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),
    # set_language view
    url('^set-language/$', 'students.views.set_language.set_language', name='set_language'),

    # User related urls
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
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
