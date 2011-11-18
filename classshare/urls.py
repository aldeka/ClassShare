from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('reviews.views',
    url(r'^$', 'home', name='home'),
    url(r'^courses/$', 'courses', name='courses'),
    
    url(r'^courses/add_or_review/$', 'add_or_review_course', name='add_or_review_course'),
    url(r'^courses/add/$', 'add_course', name='add_course'),
    
    url(r'^courses/(?P<course_id>\d+)/$', 'course', name="course"),
    url(r'^courses/(?P<course_id>\d+)/choose_class/$', 'choose_class_to_review', name='choose_class'),
    url(r'^courses/(?P<class_id>\d+)/review/$', 'review_course', name="review_course"),
    url(r'^courses/(?P<class_id>\d+)/review/(?P<review_id>\d+)/edit/$', 'edit_review', name="edit_review"),
    
    url(r'^depts/$', 'departments', name='departments'),  
    url(r'^depts/(?P<dept_abb>.+)/$', 'department', name='department'),
    
    url(r'^instructors/$', 'instructors', name='instructors'),     
    url(r'^instructors/(?P<instructor_id>\d+)/$', 'instructor', name='instructor'),
    
    url(r'^tags/$', 'tags', name='tags'),
    url(r'^tags/(?P<tag_id>\d+)/$', 'tag', name='tag'),
    
    url(r'^allreviews/$', 'reviews', name='reviews'),
    
    url(r'^students/$', 'students', name='students'),     
    url(r'^students/(?P<student_id>\d+)/$', 'student', name='student'),

    url(r'^logout/$', 'logout_page'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^admin/', include(admin.site.urls)),
)
