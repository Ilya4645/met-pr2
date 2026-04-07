from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.db import models, transaction
from django import forms
from django.views import View
from .forms import TeacherForm, TeacherInfoForm, CourseForm, StudentForm
from .models import Teacher, Course, Student, TeacherInfo


def index(request):
    """Главная страница."""
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'index.html', {'courses': courses[:2], "teachers": teachers[:2]})


def teachers(request):
    teachers = Teacher.objects.prefetch_related('course').all()
    min_courses = 2
    teachers_with_many_courses = Teacher.objects.annotate(num_courses=models.Count('course')).filter(num_courses__gt=min_courses)
    teachers_without_profile = Teacher.objects.filter(info__isnull=True)
    return render(request, 'teachers.html', {"teachers": teachers, 'teachers_with_many_courses': teachers_with_many_courses, 'teachers_without_profile': teachers_without_profile})

class create(View):
    """if request.method == 'POST':
        Teacher.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            departament = request.POST['departament'],
            phone_number = request.POST['phone_number'],
        )
        return redirect('index')"""

    template_name = 'create.html'
    form_class_teacher = TeacherForm
    form_class_info = TeacherInfoForm
    def get(self, request, *args, **kwargs):
        teacher_form = self.form_class_teacher()
        teacher_info_form = self.form_class_info()
        return render(request, self.template_name, {'teacher_form': teacher_form, 'teacher_info_form': teacher_info_form})

    def post(self, request, *args, **kwargs):
        teacher_form = self.form_class_teacher(request.POST)
        teacher_info_form = self.form_class_info(request.POST)

        if teacher_form.is_valid() and teacher_info_form.is_valid():
            with transaction.atomic():
                teacher_instance = teacher_form.save()
                teacher_info_instance = teacher_info_form.instance
                teacher_info_instance.teacher = teacher_instance
                teacher_info_instance.save()
            return redirect('teachers')
        else:
            return render(request, self.template_name, {'teacher_form': teacher_form, 'teacher_info_form': teacher_info_form})

class update(View):
    """if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.email = request.POST.get('email')
        teacher.departament = request.POST.get('departament')
        teacher.phone_number = request.POST.get('phone_number')
        teacher.is_active = request.POST.get('is_active')
        teacher.save()
        return redirect('index')
    return render(request, 'update.html', {'teacher': teacher})"""
    template_name = 'update.html'
    form_class_teacher = TeacherForm
    form_class_info = TeacherInfoForm

    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher_form = self.form_class_teacher()
        teacher_info_form = self.form_class_info()
        return render(request, self.template_name,
                      {'teacher_form': teacher_form, 'teacher_info_form': teacher_info_form})

    def post(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher_form = self.form_class_teacher(request.POST, instance=teacher)
        try:
            teacher_info_instance = teacher.info
            teacher_info_form = self.form_class_info(request.POST, instance=teacher_info_instance)
        except TeacherInfo.DoesNotExist:
            teacher_info_form = self.form_class_info(request.POST)

        if teacher_form.is_valid() and teacher_info_form.is_valid():
            with transaction.atomic():
                teacher_instance = teacher_form.save()
                teacher_info_instance = teacher_info_form.instance
                teacher_info_instance.teacher = teacher_instance
                teacher_info_instance.save()
            return redirect('teachers')
        else:
            return render(request, self.template_name, {'teacher_form': teacher_form, 'teacher_info_form': teacher_info_form})

def delete(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.delete()
    return redirect('index')

def teacher_detail(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    if not teacher:
        return HttpResponseNotFound("<h1>Преподаватель не найден</h1>")
    info = teacher.info
    teacher_courses = teacher.course.all()


    return render(request, 'teacher_detail.html', {'teacher': teacher, 'info': info, 'teacher_courses': teacher_courses})

def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {"courses": courses})

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        teacher = Teacher.objects.get(id=course.teacher_id) if course else None
    except Teacher.DoesNotExist:
        teacher = None
    if not course:
        return render(request, 'course_detail.html', {'course': course, 'teacher': teacher}, status=500)

    students_of_course = Student.objects.filter(courses__id=course_id)

    return render(request, 'course_detail.html', {'course': course, 'teacher': teacher, 'students_of_course': students_of_course})

class course_create(View):
    template_name = 'course_create.html'
    form_class_course= CourseForm
    def get(self, request, *args, **kwargs):
        course_form = self.form_class_course()
        return render(request, self.template_name, {'course_form': course_form})

    def post(self, request, *args, **kwargs):
        course_form = self.form_class_course(request.POST)

        if course_form.is_valid():
            course_form.save()
            Course.objects.create(teacher_id = request.POST['teacher_id'],)
            return redirect('courses')
        else:
            return render(request, self.template_name, {'course_form': course_form})

class course_update(View):

    template_name = 'course_update.html'
    form_class_course = CourseForm

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        course_form = self.form_class_course()
        return render(request, self.template_name,
                      {'course_form': course_form})

    def post(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=course_id)
        course_form = self.form_class_course(request.POST, instance=course)

        if course_form.is_valid():
            course_form.save()
            course.teacher_id = request.POST.get('teacher_id')
            course.save()
            return redirect('courses')
        else:
            return render(request, self.template_name, {'course_form': course_form})

def course_delete(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('courses')

def students(request):
    students = Student.objects.all()
    students_without_courses = Student.objects.filter(courses__isnull=True)
    return render(request, 'students.html', {"students": students, 'students_without_courses': students_without_courses})

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    courses_on_students = student.courses.all()
    if not student:
        return render(request, 'student_detail.html', {'student': student, 'courses_on_students': courses_on_students}, status=404)

    return render(request, 'student_detail.html', {'student': student, 'courses_on_students': courses_on_students})

def course_in_student_delete(request, student_id, course_id):
    student = Student.objects.get(id=student_id)
    course_un_student = student.courses.get(id=course_id)
    if student.courses.filter(id=course_id).exists():
        student.courses.remove(course_un_student)
        messages.success(request, 'Вы успешно отписались от курса')
    else:
        messages.error(request, 'Вы не записаны на этот курс')
    return redirect('students')

def course_in_student_create(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        if student.courses.filter(id=course_id).exists():
            return redirect('addcourse_error1')
        elif not Course.objects.filter(id=course_id).exists():
            return redirect('addcourse_error2')
        else:
            student.courses.add(course_id)
            return redirect('addcourse_success')
    return render(request, 'course_in_student_create.html', {'student': student})
class student_create(View):
    template_name = 'student_create.html'
    form_class_student = StudentForm
    def get(self, request, *args, **kwargs):
        student_form = self.form_class_student()
        return render(request, self.template_name, {'student_form': student_form})

    def post(self, request, *args, **kwargs):
        student_form = self.form_class_student(request.POST)

        if student_form.is_valid():
            cleaned_data = student_form.cleaned_data
            cleaned_data.save()
            return redirect('students')
        else:
            return render(request, self.template_name, {'student_form': student_form})


class student_update(View):

    template_name = 'student_update.html'
    form_class_student = StudentForm

    def get(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=student_id)
        student_form = self.form_class_student()
        return render(request, self.template_name,
                      {'student_form': student_form})

    def post(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(id=student_id)
        student_form = self.form_class_student(request.POST, instance=student)

        if student_form.is_valid():
            instance = student_form.save()
            return redirect('students')
        else:
            return render(request, self.template_name, {'student_form': student_form})

def student_delete(request, student_id):
    student = Student.objects.get(id=student_id)
    if student.courses.filter(id=student_id).exists():
        return redirect('student_delete_error')
    else:
        student.delete()
        return redirect('students')

def student_delete_error(request):
    return render(request, 'student_delete_error.html')

def addcourse_success(request):
    return render(request, 'addcourse_success.html')

def addcourse_error1(request):
    return render(request, 'addcourse_error1.html')

def addcourse_error2(request):
    return render(request, 'addcourse_error2.html')

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)