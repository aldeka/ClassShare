from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from reviews.models import Course
import re

def home(request):
    courses = Course.objects.all()
    return render_to_response('index.html', {'courses' : courses })
    
def add_or_review_course(request):
    # AUGH REGEX AUGHHHHH
    if request.POST:
        course_stub = request.POST('course-stub')
        stub_dept = re.search('^([a-zA-Z])+[\ ]?[0-9a-zA-Z\-\ .]+', course_stub)
        # check if this course already exists in database
        if course_id:
            review_course(request, course_id)
        # if not, add a new course
        else:
            add_course(request, stub_dept, stub_num)
        
def add_course(request, dept=None, number=None):
    return render_to_response('reviews/add_course_form.html', {'dept': dept, 'number': number})
        
def review_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # the line below is redundant, but whatever
    course_id = course.pk
    return render_to_response('reviews/review_form.html', {'course_id' : course_id })
    
def courses(request):
    courses = Course.objects.all()
    return render_to_response('reviews/course_list.html', {'courses' : courses })
    
def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render_to_response('reviews/single_course.html', {'course': course})
