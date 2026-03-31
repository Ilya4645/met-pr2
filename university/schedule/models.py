from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False)
    departament = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(max_length=100, null=False, unique=True, error_messages={'unique': "This phone_number already been registered."})
    is_active = models.BooleanField(default=True)

class TeacherInfo(models.Model):
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name='info',
        primary_key=True
    )

    bio = models.TextField(blank=True)
    academic_degree = models.CharField(blank=True)
    years_to_experience = models.PositiveSmallIntegerField(default=0)

class Course(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='course'
    )
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    start_date = models.DateField()
    end_date = models.DateField()

class Student(models.Model):
    courses = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    birth_date = models.DateField()
    email = models.EmailField(max_length=100, null=False)
    phone_number = models.CharField(max_length=100, null=False)