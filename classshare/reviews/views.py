from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from reviews.models import *
import re

def home(request):
    courses = Course.objects.all()
    return render_to_response('index.html', {'courses' : courses })
    
def add_or_review_course(request):
    '''handles the front-page form to add a new course or review an existing (autocompleted) course'''
    if request.POST:
        course_stub = request.POST('course-stub')
        # TODO: we should probably do an initial match to make sure that the input is parseable
        stub_dept = re.search('^([a-zA-Z]+)', course_stub)(0)
        stub_classnum = re.search('^[a-zA-Z]+[\ ]?([0-9]+[0-9a-zA-Z.\-]*)',course_stub)(0)
        # check if this course already exists in database
        matching_courses = Course.objects.filter(department = stub_dept, number=stub_classnum)
        if matching_courses:
            if len(matching_courses) == 1:
            # if there's a unique match
                course_id = matching_courses[0].pk
                review_course(request, course_id)
            else:
            # go to intermediate page where you choose which course you mean to edit
                choose_course_to_review(request, matching_courses)
        # if not, add a new course
        else:
            add_course(request)
        
def add_course(request):
    form = CourseForm()
    return render_to_response('reviews/add_course_form.html', {'form': form })
    
def edit_course(request, course_id):
    #TODO: This method's template doesn't exist yet, but should inherit the add_course_form.
    course = Course.objects.get(pk=course_id)
    form = CourseForm(instance=course)
    return render_to_response('reviews/edit_course_form.html', {'form': form })
    
def choose_course_to_review(request, course_set):
    data = []
    for course in course_set:
        course_dico['id'] = course.pk
        course_dico['code'] = course.course_code()
        course_dico['name'] = course.name
        data.append(course_dico)
    return render_to_response('reviews/intermediate_step.html', { 'course_data' : data })
        
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
