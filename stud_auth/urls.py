from django.conf.urls import patterns
from django.conf.urls import url

from .views import test


urlpatterns = patterns('',
                       url('^test-inner/(?P<arg>\w+)/$', test, name='test_inner'),
                      )

