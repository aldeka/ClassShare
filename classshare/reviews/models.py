from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(User):
    '''Model for all of our users, inheriting Django's built-in User model'''
    # TODO: Make LDAP connect to this thing
    is_current_student = models.BooleanField(default=True)


class Course(models.Model):
    '''Model for a given course'''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    instructor = models.ManyToManyField(Instructor, through='Class')
    

class Class(models.Model):
    '''A class is a specific instance of a course.'''
    SEMESTER_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    )
    course = models.ForeignKey(Course, blank=False)
    instructor = models.Foreignkey(Instructor, blank=False)
    year = models.IntegerField()
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES)


class Review(models.Model):
    '''Model for a single person's review of a course'''
    author = models.ForeignKey(Student, blank=True, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course)
    
    content = models.TextField(blank=True,null=True)
    is_anonymous = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Instructor(models.Model):
    '''Model for a course instructor.'''
    name = models.CharField(max_length=200)
