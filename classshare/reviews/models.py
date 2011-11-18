from django.db import models
from django import forms
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    '''Model for all of our users.'''
    user = models.OneToOneField(User)
    is_student = models.BooleanField(default=True)
    is_alumnus = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username

class Instructor(models.Model):
    '''Model for a course instructor.'''
    name = models.CharField(max_length=200)
    
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


class Tag(models.Model):
    '''Model for a user's tag for a course.'''
    name = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return 'Tag: ' + self.name

class Course(models.Model):
    '''Model for a given course'''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    department = models.ForeignKey(Department)
    number = models.CharField(max_length=12)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    
    def course_code(self):
        return self.department.abb + ' ' + self.number
    
    def __unicode__(self):
        return self.course_code()
        
    def thumbs_count(self):
        '''Calculates how many thumbs-up the course has received'''
        thumbs = 0
        classes = self.class_set.all()
        for the_class in classes:
            pos_reviews = the_class.review_set.filter
            thumbs = thumbs + len(pos_reviews)
        return thumbs
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('department','number','name','description','tags')


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

class ReviewForm(forms.ModelForm):
    # TODO: Look up how to set user for form to current user
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Review
