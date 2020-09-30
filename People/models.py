from django.db import models

# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=100, unique=True)
    contact = models.IntegerField(unique=True, blank=True, null=True)
    email = models.EmailField(
        max_length=254, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name


class Department(models.Model):
    company_name = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company')
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


BLOOD_CHOICES = (
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
    ('Single', 'Single'),
    ('Married', 'Married')
)


class People(models.Model):
    name = models.CharField(max_length=254, unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='people_company', blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='people_department', blank=True, null=True)
    contact = models.IntegerField(unique=True, blank=True)
    image = models.ImageField(upload_to="people_image/", null=True, blank=True)
    email = models.EmailField(
        max_length=254, unique=True, blank=True, null=True)
    blood_group = models.CharField(
        max_length=50, choices=BLOOD_CHOICES, blank=True, null=True)
    marital_status = models.CharField(
        max_length=50, choices=MARITAL_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    nid = models.BigIntegerField(unique=True, blank=True)
    passport = models.CharField(
        max_length=254, unique=True, blank=True, null=True)
    tracking = models.BigIntegerField(unique=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
