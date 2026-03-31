from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.db import models
from django import forms
from django.views import View
from .forms import TeacherForm
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
    form_class = TeacherForm
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data.get('email', '')
            departament = form.cleaned_data['departament']
            phone_number = form.cleaned_data['phone_number']
            bio = form.cleaned_data['bio']
            academic_degree = form.cleaned_data['academic_degree']
            years_to_experience = form.cleaned_data['years_to_experience']

            teacher = Teacher.objects.create(first_name=first_name, last_name=last_name, email=email, departament=departament, phone_number=phone_number)

            if (bio) and (academic_degree) and (years_to_experience):
                TeacherInfo.objects.create(teacher=teacher, bio=bio, academic_degree=academic_degree, years_to_experience=years_to_experience)
            return redirect('teachers')

        else:
            return render(request, self.template_name, {'form': form})

def update(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.email = request.POST.get('email')
        teacher.departament = request.POST.get('departament')
        teacher.phone_number = request.POST.get('phone_number')
        teacher.is_active = request.POST.get('is_active')
        teacher.save()
        return redirect('index')
    return render(request, 'update.html', {'teacher': teacher})

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

def course_create(request):
    if request.method == 'POST':
        Course.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            teacher_id = request.POST['teacher_id'],
        )
        return redirect('courses')
    return render(request, 'course_create.html')

def course_update(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.start_date = request.POST.get('start_date')
        course.end_date = request.POST.get('end_date')
        course.teacher_id = request.POST.get('teacher_id')
        course.save()
        return redirect('courses')
    return render(request, 'course_update.html', {'course': course})

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
def student_create(request):
    if request.method == 'POST':
        Student.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            birth_date = request.POST['birth_date'],
            email = request.POST['email'],
            phone_number = request.POST['phone_number'],
        )
        return redirect('students')
    return render(request, 'student_create.html')

def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.birth_date = request.POST.get('birth_date')
        student.email = request.POST.get('email')
        student.phone_number = request.POST.get('phone_number')
        student.save()
        return redirect('students')
    return render(request, 'student_update.html', {'student': student})

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