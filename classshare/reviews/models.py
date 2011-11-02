from django.db import models
from django.contrib.auth.models import User


class Student(User):
    '''Model for all of our users, inheriting Django's built-in User model'''
    # TODO: Make LDAP connect to this thing
    is_current_student = models.BooleanField(default=True)


class Instructor(models.Model):
    '''Model for a course instructor.'''
    name = models.CharField(max_length=200)


class Department(models.Model):
    '''Model for an academic department.'''
    name = models.CharField(max_length=200)
    # Official Abbreviation
    abb = models.CharField(max_length=10)


class Tag(models.Model):
    '''Model for a user's tag for a course.'''
    name = models.CharField(max_length=200)


class Course(models.Model):
    '''Model for a given course'''
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    department = models.ForeignKey(Department, blank=False)
    number = models.IntegerField()
    ccn = models.IntegerField(blank=True,null=True)
    tag = models.ManyToManyField(Tag)    


class Class(models.Model):
    '''A class is a specific instance of a course.'''
    SEMESTER_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    )
    course = models.ForeignKey(Course)
    instructor = models.ForeignKey(Instructor)
    year = models.IntegerField()
    semester = models.CharField(max_length=6, choices=SEMESTER_CHOICES)


class Review(models.Model):
    '''Model for a single person's review of a course'''
    author = models.ForeignKey(Student, blank=True, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Class)    
    content = models.TextField(blank=True,null=True)
    is_anonymous = models.BooleanField(default=False)
    thumbs_up = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
