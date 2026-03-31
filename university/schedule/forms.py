from django import forms
from .models import Teacher

class TeacherForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}),
                                 help_text='Введите имя преподавателя')
    last_name = forms.CharField(label='Фамилия', max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
                                 help_text='Введите фамилию преподавателя')
    email = forms.EmailField(label='Почта', required=False, max_length=100,
                                widget=forms.EmailInput(attrs={'placeholder': 'Введите почту'}),
                                help_text='Введите почту преподавателя')
    departament = forms.CharField(label='Кафедра', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите кафедру'}),
                                help_text='Введите кафедру преподавателя')
    phone_number = forms.CharField(label='Контактный телефон', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите контактный телефон'}),
                                help_text='Введите контактный телефон преподавателя')
    bio = forms.CharField(label='Профессия', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите профессию'}),
                                help_text='Введите профессию преподавателя')
    academic_degree = forms.CharField(label='Ученая степень', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите ученую степень'}),
                                help_text='Введите ученую степень преподавателя')
    years_to_experience = forms.IntegerField(label='Стаж работы',
                                      widget=forms.TextInput(attrs={'placeholder': 'Введите стаж работы'}),
                                      help_text='Введите стаж работы преподавателя')