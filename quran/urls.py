from django.conf.urls.defaults import *
from views import show_ayat

urlpatterns = patterns('',
    url(r's(?P<surah_num>\d+)/a(?P<ayat_num>\d+)/(?P<translator>[-\w]+)$', show_ayat),
)
