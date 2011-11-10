from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from reviews.models import *

def home(request):
    courses = Course.objects.all()
    return render_to_response('index.html', {'courses' : courses },
                              context_instance=RequestContext(request))
    
def courses(request):
    courses = Course.objects.all()
    return render_to_response('reviews/course_list.html', {'courses' : courses },
                              context_instance=RequestContext(request))
    
def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    instructors = set()
    for reviewed_class in course.class_set.all():
        instructors.add(reviewed_class.instructor)
    course.instructors = list(instructors)
    return render_to_response('reviews/single_course.html', {'course': course},
                              context_instance=RequestContext(request))

def departments(request):
    departments = Department.objects.all()
    return render_to_response('reviews/department_list.html', {'departments': departments},
                              context_instance=RequestContext(request))

def department(request, dept_abb):
    dept_abb = dept_abb.upper()
    dept = get_object_or_404(Department, pk=dept_abb)
    return render_to_response('reviews/single_department.html', {'department': dept},
                              context_instance=RequestContext(request))

def instructors(request):
    instructors = Instructor.objects.all()
    return render_to_response('reviews/instructor_list.html', {'instructors': instructors},
                              context_instance=RequestContext(request))

def instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    courses = set()
    for reviewed_class in instructor.class_set.all():
        courses.add(reviewed_class.course)
    instructor.courses = list(courses)
    return render_to_response('reviews/single_instructor.html', {'instructor': instructor},
                              context_instance=RequestContext(request))

def tags(request):
    tags = Tag.objects.all()
    return render_to_response('reviews/tag_list.html', {'tags': tags},
                              context_instance=RequestContext(request))

def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    return render_to_response('reviews/single_tag.html', {'tag': tag},
                              context_instance=RequestContext(request))

# TODO: Do we need this view?
def reviews(request):
    reviews = Review.objects.all()
    return render_to_response('reviews/review_list.html', {'reviews': reviews},
                              context_instance=RequestContext(request))

def students(request):
    students = Student.objects.all()
    return render_to_response("reviews/student_list.html",{'students': students},
                              context_instance=RequestContext(request))

def student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    courses = set()
    for review in student.review_set.all():
        courses.add(review.reviewed_class.course)
    student.courses = list(courses)
    return render_to_response('reviews/single_student.html', {'student': student},
                              context_instance=RequestContext(request))

def logout_page(request):
    """Log users out and re-direct them to the login page."""
    logout(request)
    return HttpResponseRedirect('/login')
