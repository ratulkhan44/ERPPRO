from django.db import models

from django.contrib.auth.models import AbstractUser
from People.models import Company, Department

# Create your models here.

class UserRole(models.Model):

    user_role = models.CharField(max_length=254,unique=True)
    

    def __str__(self):
        return self.user_role


BLOOD_CHOICES = (
    ('', '--Select--'),
    ('A+', 'A+'),
    ('O+', 'O+'),
    ('B+', 'B+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('O-', 'O-'),
    ('B-', 'B-'),
    ('AB-', 'AB-'),
)

MARITAL_CHOICES = (
    #('', '--Select--'),
    ('Unmarried', 'Unmarried'),
    ('Married', 'Married')
)

class CustomUser(AbstractUser):
    user_role =models.ForeignKey(
        UserRole,on_delete=models.CASCADE,related_name='user_userrole'
            )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='user_company', null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='user_department', null=True)
    full_name = models.CharField(max_length=220)
    contact_no = models.BigIntegerField(unique=True, default=None)
    nid = models.CharField(max_length=220, blank=True, null=True)
    passport = models.CharField(max_length=220, blank=True, null=True)
    dob = models.DateField(null=True)
    marital_status = models.CharField(max_length=240, choices=MARITAL_CHOICES,default=None, null=True)
    blood_group = models.CharField(max_length=240, choices=BLOOD_CHOICES,default=None, blank=True, null=True)
    job_title = models.CharField(max_length=240, null=True)
    work_location = models.CharField(max_length=220,null=True)
    profile_pic = models.ImageField(upload_to='user_images/', null=True, blank=True)   

    def __str__(self):
        return self.full_name
