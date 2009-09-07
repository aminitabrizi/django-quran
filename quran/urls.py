from django.conf.urls.defaults import *

urlpatterns = patterns('quran.views',
    url(r'/s(?P<surah>\d+)/a(?P<ayat>\d+)$'),
)
