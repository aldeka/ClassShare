from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.contrib.auth.models import User
import datetime

class Instructor(models.Model):
    '''Model for a course instructor.'''
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class InstructorForm(forms.ModelForm):

    class Meta:
        model = Instructor

class Department(models.Model):
    '''Model for an academic department.'''
    name = models.CharField(max_length=200, blank=True,null=True)
    # Official Abbreviation, also used as primary key
    abb = models.CharField(max_length=10, primary_key=True)
    # Link to official site
    link = models.URLField(null=True, blank=True)
    
    class Meta:
        ordering = ['abb']
    
    def __unicode__(self):
        return self.abb

class Course(models.Model):
    '''Model for a given course'''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    department = models.ForeignKey(Department)
    number = models.CharField(max_length=12)
    units = models.IntegerField(blank=True,null=True)
    
    def course_code(self):
        return self.department.abb + ' ' + self.number
    
    def __unicode__(self):
        return self.course_code()

    def review_count(self):
        reviews = 0
        for cls in self.class_set.all():
            reviews += len(cls.review_set.all())
        return reviews
        
    def all_instructors(self):
        '''Returns all the instructors that have ever taught the course'''
        instructors = []
        for the_class in self.class_set.all():
            if the_class.instructor not in instructors and the_class.instructor is not None:
                instructors.append(the_class.instructor)
        return instructors
        
    def thumbs_count(self):
        '''Calculates how many thumbs-up the course has received'''
        thumbs = 0
        classes = self.class_set.all()
        for the_class in classes:
            pos_reviews = the_class.review_set.filter(thumbs_up=True)
            thumbs += len(pos_reviews)
        return thumbs

    def tags(self):
        return Tag.objects.filter(reviews__reviewed_class__course__id=self.pk)


def get_courses(department=None, instructor=None, semester=None, tags=[],
                units=None, year=None):
    """Retrieve courses matching various filters specified by the user.
    Arguments:
      department: Department object
      instructor: Instructor object
      semester: String representing the semester, e.g. "Fall"
      tags: list of tag strings or tag objects
      units: Integer representing number of units
      year: Integer representing year class was offered."""
    courses = Course.objects.all()
    if department:
        courses = courses.filter(department=department)
    if instructor:
        courses = courses.filter(instructor=instructor)
    if semester:
        semester = semester.capitalize()
        courses = courses.filter(class__semester=semester)
    if tags:
        courses = courses.filter(class__review__tag__name__in=tags)
    if units:
        courses = courses.filter(units=units)
    if year:
        courses = courses.filter(class__year__exact=year)
    return courses
        

        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('department','number','name','description')


class Class(models.Model):
    '''A class is a specific instance of a course.'''
    SEMESTER_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    )
    course = models.ForeignKey(Course)
    instructor = models.ForeignKey(Instructor, blank=True, null=True)
    year = models.IntegerField()
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES)
    
    class Meta:
        ordering = ['-year']
        verbose_name_plural = "classes"
    
    def semester_formatted(self):
        '''Returns a nicely formatted semester string, e.g. "Fall 2008"'''
        return self.semester + ' ' + str(self.year)
    
    def __unicode__(self):
        return self.course.course_code() + ': ' + self.semester_formatted()
    
    def semester2date(self):
        '''Returns a datetime for the rough beginning date of the class' semester'''
        # default value is 8, for August
        month = 8
        if self.semester == 'Spring':
            month = 1
        elif self.semester == 'Summer':
            month = 5
        return datetime.date(self.year, month, 15)

class ClassForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Class
        fields = ('course', 'year', 'semester', 'instructor')

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        # Reload instructor options when form is created, in case new ones have been added
        self.fields['instructor'].queryset = Instructor.objects.all()



class Review(models.Model):
    '''Model for a single person's review of a course'''
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    reviewed_class = models.ForeignKey(Class)
    content = models.TextField(blank=True,null=True)
    is_anonymous = models.BooleanField(default=False)
    thumbs_up = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __unicode__(self):
        return self.author.username + "'s review of " + str(self.reviewed_class)

class Tag(models.Model):
    '''Model for a user's tag for a course.'''
    name = models.CharField(max_length=200, primary_key=True)
    reviews = models.ManyToManyField(Review, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name


class MultiStringField(forms.CharField):
    """Form field for comma-separated values such as tags."""

    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        # Convert to lower case and trim whitespace
        return [s.strip() for s in value.lower().split(',')]


class ReviewForm(forms.ModelForm):
    # TODO: Look up how to set user for form to current user.
    # http://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    tags = MultiStringField()
    class Meta:
        model = Review
