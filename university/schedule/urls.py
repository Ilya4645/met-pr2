from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='index'),
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/create', views.create, name='create'),
    path('teachers/update/<int:teacher_id>', views.update, name='update'),
    path('teachers/delete/<int:teacher_id>', views.delete, name='delete'),
    path('teachers/detail/<int:teacher_id>', views.teacher_detail, name='teacher_detail'),
    path('courses/', views.courses, name='courses'),
    path('courses/detail/<int:course_id>', views.course_detail, name='course_detail'),
]
