from django.shortcuts import render_to_response
from reviews.models import Course

def home(request):
    courses = Course.objects.all()
    return render_to_response('index.html', {'courses' : courses })
    
def courses(request):
    courses = Course.objects.all()
    return render_to_response('reviews/course_list.html', {'courses' : courses })
    
def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render_to_response('reviews/single_course.html', {'course': course})
