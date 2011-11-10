from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
import datetime

class Student(User):
    '''Model for all of our users, inheriting Django's built-in User model'''
    # TODO: Make LDAP connect to this thing
    is_alumnus = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Instructor(models.Model):
    '''Model for a course instructor.'''
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return 'Instructor: ' + self.name

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
        return self.abb + ' department'


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
    department = models.ForeignKey(Department, blank=False)
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
        
class CourseForm(ModelForm):
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
    ccn = models.IntegerField(blank=True,null=True)
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

class Review(models.Model):
    '''Model for a single person's review of a course'''
    author = models.ForeignKey(Student, blank=True, null=True, on_delete=models.SET_NULL)
    reviewed_class = models.ForeignKey(Class)
    content = models.TextField(blank=True,null=True)
    is_anonymous = models.BooleanField(default=False)
    thumbs_up = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __unicode__(self):
        return author.name + "'s review of " + self.reviewed_class
