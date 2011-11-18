from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from reviews.models import *
import re

def home(request):
    courses = Course.objects.all()
    return render(request, 'index.html', {'courses' : courses })

@login_required
def add_or_review_course(request):
    '''handles the front-page form to add a new course or review an existing (autocompleted) course'''
    if request.method == "POST":
        course_stub = request.POST.__getitem__('course-stub')
        # TODO: we should probably do an initial match to make sure that the input is parseable
        stub_dept = re.search('^([a-zA-Z]+)', course_stub).group(0).upper()
        stub_classnum = re.search('[\ ]*([0-9]+[0-9a-zA-Z.\-]*)', course_stub).group(1)
        # check if this course already exists in database
        matching_courses = Course.objects.filter(department = stub_dept, number=stub_classnum)
        if matching_courses:
            if len(matching_courses) == 1:
            # if there's a unique match
                course_id = matching_courses[0].pk
                return redirect("choose_class", course_id=course_id)
            else:
            # go to intermediate page where you choose which course you mean to edit
                return choose_course_to_review(request, matching_courses)
        # if not, add a new course
        else:
            return redirect("add_course")
        

@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course, created = Course.objects.get_or_create(
                name = form.cleaned_data["name"],
                description = form.cleaned_data["description"],
                department = form.cleaned_data["department"],
                number = form.cleaned_data["number"])
            if created:
                messages.success(request, "Added new course: %s", course.course_code())
            return redirect("choose_class", course.id)
    else:
        # TODO: Prepopulate with whatever they input into the search form
        form = CourseForm()
    return render(request, 'reviews/add_course_form.html', { 'form': form })

@login_required
def edit_course(request, course_id):
    #TODO: This method's template doesn't exist yet, but should inherit the add_course_form.
    course = Course.objects.get(pk=course_id)
    form = CourseForm(instance=course)
    return render(request, 'reviews/edit_course_form.html', {'form': form })

@login_required
def choose_course_to_review(request, course_set):
    data = []
    for course in course_set:
        course_dico['id'] = course.pk #TODO: course_dico isn't created anywhere
        course_dico['code'] = course.course_code()
        course_dico['name'] = course.name
        data.append(course_dico)
    # TODO: Name template something else
    return render(request, 'reviews/intermediate_step.html', { 'course_data' : data })

@login_required
def choose_class_to_review(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            cls, created = Class.objects.get_or_create(
                course = form.cleaned_data["course"],
                instructor = form.cleaned_data["instructor"],
                year = form.cleaned_data["year"],
                semester = form.cleaned_data["semester"])
            return redirect("review_course", cls.id)
    else:
        # TODO: Restrict instructor options to those who have taught the course.
        # TODO: Allow users to add an instructor from this page
        form = ClassForm(initial={'course': course})
    return render(request, 'reviews/choose_class_form.html', {'form': form, 'course': course})


@login_required
def review_course(request, class_id):
    reviewed_class = get_object_or_404(Class, pk=class_id)
    if request.method =="POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save()
            course_id = new_review.reviewed_class.course.id
            return redirect("course", course_id)
    else:
        form = ReviewForm(initial={'author': request.user, 'reviewed_class': class_id})
    return render(request, 'reviews/review_form.html', {'form': form, 'class' : reviewed_class })

@login_required
def courses(request):
    courses = Course.objects.all()
    return render(request, 'reviews/course_list.html', {'courses' : courses})

@login_required
def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    instructors = set()
    for reviewed_class in course.class_set.all():
        instructors.add(reviewed_class.instructor)
    course.instructors = list(instructors)
    return render(request, 'reviews/single_course.html', {'course': course})

@login_required
def departments(request):
    departments = Department.objects.all()
    return render(request, 'reviews/department_list.html', {'departments': departments})

@login_required
def department(request, dept_abb):
    dept_abb = dept_abb.upper()
    dept = get_object_or_404(Department, pk=dept_abb)
    return render(request, 'reviews/single_department.html', {'department': dept})

@login_required
def instructors(request):
    instructors = Instructor.objects.all()
    return render(request, 'reviews/instructor_list.html', {'instructors': instructors})

@login_required
def instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    courses = set()
    for reviewed_class in instructor.class_set.all():
        courses.add(reviewed_class.course)
    instructor.courses = list(courses)
    return render(request, 'reviews/single_instructor.html', {'instructor': instructor})

@login_required
def add_instructor(request):
    if request.method == "POST":
        form = InstructorForm(request.POST)
        if form.valid():
            instructor, created = Instructor.objects.get_or_create(name = form.cleaned_data["name"])
    else:
        form = InstructorForm()
    return render(request, 'reviews/instructor_form.html', {'form': form})

@login_required
def tags(request):
    tags = Tag.objects.all()
    return render(request, 'reviews/tag_list.html', {'tags': tags})

@login_required
def tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    return render(request, 'reviews/single_tag.html', {'tag': tag})

# TODO: Do we need this view?
def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

@login_required
def students(request):
    students = UserProfile.objects.filter(is_student=True)
    return render(request, "reviews/student_list.html", {'students': students})

@login_required
def student(request, student_id):
    student = get_object_or_404(UserProfile, pk=student_id)
    courses = set()
    for review in student.user.review_set.all():
        courses.add(review.reviewed_class.course)
    student.courses = list(courses)
    return render(request, 'reviews/single_student.html', {'student': student})

def logout_page(request):
    """Log users out and re-direct them to the login page."""
    logout(request)
    return redirect('login')
