from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG

from students.views.students import StudentUpdateView, StudentDeleteView, StudentList
from students.views.students import students_ajax_next_page
from students.views.custom_contact_form import CustomContactFormView
from students.views.contact_admin import ContactAdminView
from students.views.groups import GroupsDeleteView

#test
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$',
        'students.views.students_add.students_add', name='students_add'),
#    url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.students.students_edit', name='students_edit'),
#    url(r'^students/(?P<sid>\d+)/delete/$', 'students.views.students.students_delete', name='students_delete'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        StudentUpdateView.as_view(), name='students_edit'),
    url(r'^(?P<pk>\d+)/delete/$',
        StudentDeleteView.as_view(),
        name='students_delete'),
    url(r'^student_list/$', StudentList.as_view()),

    # trying ajax
    url(r'students/next_page$',
        students_ajax_next_page, name='students_ajax_next_page'),
    #test templateView
    url('^test/$', RedirectView.as_view(pattern_name="home")),

    #Groups urls
    url(r'^groups/$',
        'students.views.groups.groups_list', name='groups'),
    url(r'^groups/add/$',
        'students.views.groups.groups_add', name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$',
        'students.views.groups.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', 
        GroupsDeleteView.as_view(), name='groups_delete'),

    # Journal url
    url(r'^journal/$', 'students.views.journal.journal_list', name='journal'),

    url(r'^admin/', include(admin.site.urls)),

    # Contact Admin Form
    url(r'^contact-admin/$', ContactAdminView.as_view(),
        name='contact_admin'),
    # contact admin with application django-contact-form
    #url(r'^contact-form/$', include('contact_form.urls')),
    url(r'^contact-form/$',
        CustomContactFormView.as_view(), name='contact_form'),
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
