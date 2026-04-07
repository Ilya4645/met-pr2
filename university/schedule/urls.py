from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='index'),
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/create', views.create.as_view(), name='create'),
    path('teachers/update/<int:teacher_id>', views.update.as_view(), name='update'),
    path('teachers/delete/<int:teacher_id>', views.delete, name='delete'),
    path('teachers/detail/<int:teacher_id>', views.teacher_detail, name='teacher_detail'),
    path('courses/', views.courses, name='courses'),
    path('courses/detail/<int:course_id>', views.course_detail, name='course_detail'),
    path('courses/create', views.course_create.as_view(), name='course_create'),
    path('courses/update/<int:course_id>', views.course_update.as_view(), name='course_update'),
    path('courses/delete/<int:course_id>', views.course_delete, name='course_delete'),
    path('students/', views.students, name='students'),
    path('students/detail/<int:student_id>', views.student_detail, name='student_detail'),
    path('students/create', views.student_create.as_view(), name='student_create'),
    path('students/deletecourse/<int:student_id>/<int:course_id>', views.course_in_student_delete, name='course_in_student_delete'),
    path('students/addcourse/<int:student_id>', views.course_in_student_create, name='course_in_student_create'),
    path('students/addcourse_success', views.addcourse_success, name='addcourse_success'),
    path('students/addcourse_error', views.addcourse_error1, name='addcourse_error1'),
    path('students/addcourse_notfound', views.addcourse_error2, name='addcourse_error2'),
    path('students/update/<int:student_id>', views.student_update.as_view(), name='student_update'),
    path('students/delete/<int:student_id>', views.student_delete, name='student_delete'),
    path('students/delete/error', views.student_delete_error, name='student_delete_error'),

]
