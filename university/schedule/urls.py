from . import views
from django.urls import path, re_path

urlpatterns = [
    path('teachers/', views.index, name='index'),
]
