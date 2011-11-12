from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from reviews.models import *
import re

def home(request):
    courses = Course.objects.all()
    return render_to_response('index.html', {'courses' : courses }, context_instance=RequestContext(request))

@login_required
def add_or_review_course(request):
    '''handles the front-page form to add a new course or review an existing (autocompleted) course'''
    if request.POST:
        course_stub = request.POST.__getitem__('course-stub')
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

@login_required
def add_course(request):
    form = CourseForm()
    return render_to_response('reviews/add_course_form.html', {'form': form }, context_instance=RequestContext(request))

@login_required
def edit_course(request, course_id):
    #TODO: This method's template doesn't exist yet, but should inherit the add_course_form.
    course = Course.objects.get(pk=course_id)
    form = CourseForm(instance=course)
    return render_to_response('reviews/edit_course_form.html', {'form': form }, context_instance=RequestContext(request))

@login_required
def choose_course_to_review(request, course_set):
    data = []
    for course in course_set:
        course_dico['id'] = course.pk
        course_dico['code'] = course.course_code()
        course_dico['name'] = course.name
        data.append(course_dico)
    return render_to_response('reviews/intermediate_step.html', { 'course_data' : data },
                              context_instance=RequestContext(request))

@login_required
def review_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # the line below is redundant, but whatever
    course_id = course.pk
    return render_to_response('reviews/review_form.html', {'course_id' : course_id }, context_instance=RequestContext(request))

@login_required
def courses(request):
    message = ''
    if request.POST:
    # if we just created a new course
        f = CourseForm(request.POST)
        new_course = f.save()
        message = 'New course saved'
    courses = Course.objects.all()
    return render_to_response('reviews/course_list.html', {'courses' : courses, 'message' : message },
                              context_instance=RequestContext(request))

@login_required
def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    instructors = set()
    for reviewed_class in course.class_set.all():
        instructors.add(reviewed_class.instructor)
    course.instructors = list(instructors)
    return render_to_response('reviews/single_course.html', {'course': course},
                              context_instance=RequestContext(request))

@login_required
def departments(request):
    departments = Department.objects.all()
    return render_to_response('reviews/department_list.html', {'departments': departments},
                              context_instance=RequestContext(request))

@login_required
def department(request, dept_abb):
    dept_abb = dept_abb.upper()
    dept = get_object_or_404(Department, pk=dept_abb)
    return render_to_response('reviews/single_department.html', {'department': dept},
                              context_instance=RequestContext(request))

@login_required
def instructors(request):
    instructors = Instructor.objects.all()
    return render_to_response('reviews/instructor_list.html', {'instructors': instructors},
                              context_instance=RequestContext(request))

@login_required
def instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    courses = set()
    for reviewed_class in instructor.class_set.all():
        courses.add(reviewed_class.course)
    instructor.courses = list(courses)
    return render_to_response('reviews/single_instructor.html', {'instructor': instructor},
                              context_instance=RequestContext(request))

@login_required
def tags(request):
    tags = Tag.objects.all()
    return render_to_response('reviews/tag_list.html', {'tags': tags},
                              context_instance=RequestContext(request))

@login_required
def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    return render_to_response('reviews/single_tag.html', {'tag': tag},
                              context_instance=RequestContext(request))

# TODO: Do we need this view?
def reviews(request):
    reviews = Review.objects.all()
    return render_to_response('reviews/review_list.html', {'reviews': reviews},
                              context_instance=RequestContext(request))

@login_required
def students(request):
    students = UserProfile.objects.filter(is_student=True)
    return render_to_response("reviews/student_list.html",{'students': students},
                              context_instance=RequestContext(request))

@login_required
def student(request, student_id):
    student = get_object_or_404(UserProfile, pk=student_id)
    courses = set()
    for review in student.user.review_set.all():
        courses.add(review.reviewed_class.course)
    student.courses = list(courses)
    return render_to_response('reviews/single_student.html', {'student': student},
                              context_instance=RequestContext(request))

def logout_page(request):
    """Log users out and re-direct them to the login page."""
    logout(request)
    return HttpResponseRedirect('/login')
