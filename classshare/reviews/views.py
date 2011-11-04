from django.shortcuts import render_to_response, get_object_or_404
from reviews.models import *

def home(request):
    courses = Course.objects.all()
    return render_to_response('index.html', {'courses' : courses })
    
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

def instructors(request):
    instructors = Instructor.objects.all()
    return render_to_response('reviews/instructor_list.html', {'instructors': instructors})

def instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    courses = set()
    for reviewed_class in instructor.class_set.all():
        courses.add(reviewed_class.course)
    instructor.courses = list(courses)
    return render_to_response('reviews/single_instructor.html', {'instructor': instructor})

def tags(request):
    tags = Tag.objects.all()
    return render_to_response('reviews/tag_list.html',{'tags':tags})

def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    courses = set()
    courses = tag.course_set.all()
    tag.courses = list(courses)
    return render_to_response('reviews/single_tag.html', {'tag': tag})

def reviews(request):
    reviews = Reviews.objects.all()
    return render_to_response('reviews/reviews_list.html', {'reviews':reviews})
