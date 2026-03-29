from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Teacher, Course


def index(request):
    """Главная страница."""
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'index.html', {'courses': courses[:2], "teachers": teachers[:2]})


def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {"teachers": teachers})

def create(request):
    if request.method == 'POST':
        Teacher.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            departament = request.POST['departament'],
            phone_number = request.POST['phone_number'],
        )
        return redirect('index')
    return render(request, 'create.html')

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
    teacher = Teacher.objects.get(id=course.teacher_id) if course else None
    if not course:
        return render(request, 'course_detail.html', {'course': course, 'teacher': teacher}, status=404)

    return render(request, 'course_detail.html', {'course': course, 'teacher': teacher})

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)