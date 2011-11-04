from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'reviews.views.home', name='home'),
    url(r'^courses/$', 'reviews.views.courses', name='courses'),
    url(r'^courses/add/$', 'reviews.views.add_or_review_course', name='add_or_review_course'),
    url(r'^courses/(?P<course_id>\d+)/$', 'reviews.views.course', name="course"),
    url(r'^courses/(?P<course_id>\d+)/review/$', 'reviews.views.write_new_review', name="write_new_review"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
