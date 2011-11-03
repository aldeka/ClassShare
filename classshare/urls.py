from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'reviews.views.home', name='home'),
    url(r'^courses/$', 'reviews.views.courses', name='courses'),
    url(r'^courses/(?P<course_id>\d+)/$', 'reviews.views.course', name="course"),
    url(r'^depts/(?P<dept_abb>\w+)/$', 'reviews.views.department', name='department'),
    url(r'^instructors/(?P<instructor_id>\d+)/$', 'reviews.views.instructor', name='instructor'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
