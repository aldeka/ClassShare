from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from reviews.models import *
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
    instructors = set()
    for reviewed_class in course.class_set.all():
        instructors.add(reviewed_class.instructor)
    course.instructors = list(instructors)
    return render_to_response('reviews/single_course.html', {'course': course})

def departments(request):
    departments = Department.objects.all()
    return render_to_response('reviews/department_list.html', {'departments': departments})

def department(request, dept_abb):
    dept_abb = dept_abb.upper()
    dept = get_object_or_404(Department, pk=dept_abb)
    return render_to_response('reviews/single_department.html', {'department': dept})

def instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    courses = set()
    for reviewed_class in instructor.class_set.all():
        courses.add(reviewed_class.course)
    instructor.courses = list(courses)
    return render_to_response('reviews/single_instructor.html', {'instructor': instructor})
