from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

def validate_phone_number(value):
    if not value.replace('+', '').isdigit() and value != '':
        raise ValidationError('Номер телефона должен содержать только цифры и знак +')

def validate_no_numbers(value):
    if re.search(r'\d', value):
        raise ValidationError('Это поле не должно содержать цифр')

def validate_min_words(value):
    if len(value.split()) < 3:
        raise ValidationError('Это поле должно содержать минимум 3 слова')

def validate_start_with_letter(value):
    if not value or not value[0].isalpha():
        raise ValidationError('Это поле должно начинаться с буквы')

class Teacher(models.Model):
    first_name = models.CharField(max_length=100, null=False, validators=[validate_no_numbers, validate_start_with_letter], verbose_name="Имя")
    last_name = models.CharField(max_length=100, null=False, validators=[validate_no_numbers, validate_start_with_letter], verbose_name="Фамилия")
    birth_date = models.DateField(null=True, verbose_name="Дата рождения")
    email = models.EmailField(max_length=100, null=False, verbose_name="Электронная почта")
    departament = models.CharField(max_length=100, null=False, validators=[validate_min_words, validate_start_with_letter], verbose_name="Кафедра")
    phone_number = models.CharField(max_length=100, null=False, unique=True, error_messages={'unique': "This phone_number already been registered."}, validators=[validate_phone_number], verbose_name="Номер телефона")
    pass_serial = models.CharField(max_length=4, null=True, unique=True, error_messages={'unique': "This pass serial already been registered."}, verbose_name="Серия паспорта")
    pass_number = models.CharField(max_length=6, null=True, error_messages={'unique': "This pass number already been registered."}, verbose_name="Номер паспорта")
    pass_date = models.DateField(verbose_name="Дата выдачи паспорта")
    pass_issued = models.CharField(max_length=100, null=True, validators=[validate_min_words], verbose_name="Кем выдан паспорт?")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")

class TeacherInfo(models.Model):
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name='info',
        primary_key=True
    )

    bio = models.TextField(blank=True, verbose_name="Должность")
    academic_degree = models.CharField(blank=True, verbose_name="Ученая степень")
    years_to_experience = models.PositiveSmallIntegerField(default=0, verbose_name="Стаж работы (в годах)")
    education = models.TextField(blank=True, verbose_name="Образование")
    date_of_employment = models.DateField(verbose_name="Дата трудоустройства")
    marital_status = models.TextField(blank=True, verbose_name="Семейное положение")
    registration_address = models.TextField(blank=True, verbose_name="Адрес регистрации")
    residential_address = models.TextField(blank=True, verbose_name="Адрес фактического проживания")

class Course(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='course'
    )
    title = models.CharField(max_length=100, null=False, validators=[validate_no_numbers, validate_start_with_letter], verbose_name="Наименование курса")
    min_description = models.CharField(max_length=30, verbose_name="Краткое описание курса")
    description = models.TextField(null=False, validators=[validate_min_words], verbose_name="Подробное описание курса")
    start_date = models.DateField(default=timezone.now, verbose_name="Дата начала курса")
    end_date = models.DateField(default=timezone.now, verbose_name="Дата окончания курса")


class Student(models.Model):
    courses = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=100, null=False, validators=[validate_no_numbers, validate_start_with_letter], verbose_name="Имя")
    last_name = models.CharField(max_length=100, null=False, validators=[validate_no_numbers, validate_start_with_letter], verbose_name="Фамилия")
    birth_date = models.DateField(null=True, verbose_name="Дата рождения")
    email = models.EmailField(max_length=100, null=False, verbose_name="Электронная почта")
    phone_number = models.CharField(max_length=100, null=False, validators=[validate_phone_number], verbose_name="Контактный номер телефона")
    pass_serial = models.CharField(max_length=4, null=True, unique=True, error_messages={'unique': "This pass serial already been registered."}, verbose_name="Серия паспорта")
    pass_number = models.CharField(max_length=10, null=True, error_messages={'unique': "This pass number already been registered."}, verbose_name="Номер паспорта")
    pass_date = models.DateField(default=timezone.now, verbose_name="Дата выдачи паспорта")
    pass_issued = models.CharField(max_length=100, null=True, validators=[validate_min_words], verbose_name="Кем выдан паспорт?")
    registration_address = models.TextField(blank=True, null=True, verbose_name="Адрес регистрации")
    residential_address = models.TextField(blank=True, null=True, verbose_name="Адрес фактического проживания")