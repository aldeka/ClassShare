from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class ISchooler(User):
    '''Model for all of our users, inheriting Django's built-in User model'''
    # TODO: Make LDAP connect to this thing
    is_current_student = models.BooleanField(default=True)

class Course(models.Model):
    '''Model for a given course'''
    # TODO: decide if we want another model for each instance of the course ("Class?")
    name = models.CharField(max_length=200)

class Review(models.Model):
    '''Model for a single person's review of a course'''
    author = models.ForeignKey(ISchooler, blank=True, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course)
    
    content = models.TextField(blank=True,null=True)
    is_anonymous = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
