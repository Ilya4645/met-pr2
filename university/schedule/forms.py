from django import forms
from .models import Teacher, TeacherInfo, Course, Student
from django.core.exceptions import ValidationError

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

class TeacherForm(forms.ModelForm):
    """first_name = forms.CharField(label='Имя', max_length=100,
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
                                      help_text='Введите стаж работы преподавателя')"""
    email = forms.EmailField(label='Электронная почта', required=False, max_length=100,
                             widget=forms.EmailInput(attrs={'placeholder': 'Введите почту'}))
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'departament', 'phone_number', 'is_active', 'birth_date', 'pass_serial', 'pass_number', 'pass_date',
                  'pass_issued']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя преподавателя', 'class': 'form_control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия преподавателя', 'class': 'form_control'}),
            'departament': forms.TextInput(
                attrs={'placeholder': 'Кафедра', 'class': 'form_control'}),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Формат +7XXXXXXXXXX', 'class': 'form_control'}),
            'birth_date': forms.DateInput(attrs={'placeholder': 'Дата рождения', 'class': 'form_control', 'type': 'date'}),
            'pass_serial': forms.TextInput(
                attrs={'placeholder': 'Серия паспорта (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'}),
            'pass_number': forms.TextInput(
                attrs={'placeholder': 'Номер паспорта (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'}),
            'pass_date': forms.DateInput(
                attrs={'placeholder': 'Дата выдачи паспорта (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control', 'type': 'date'}),
            'pass_issued': forms.TextInput(
                attrs={'placeholder': 'Кем выдан паспорт (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'})
        }

        is_active = forms.BooleanField(label='Активен?', widget=forms.TextInput(attrs={'placeholder': '0-не активен, 1-активен', 'class': 'form_control'}))

    def clean_first_name(self):
         return self.cleaned_data["first_name"].strip().capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        last_name = last_name.capitalize()
        return last_name

    def clean_departament(self):
        departament = self.cleaned_data["departament"]
        departament = departament[0].capitalize() + departament[1:]
        return departament

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and last_name and first_name.lower() == last_name.lower():
            self.add_error("last_name", 'Имя и фамилия не должны совпадать')

class TeacherInfoForm(forms.ModelForm):

    academic_degree = forms.ChoiceField(label='Ученая степень',
        choices=(
            ('1', 'Ассистент'),
            ('2', 'Старший преподаватель'),
            ('3', 'Доцент'),
            ('4', 'Профессор'),
        ))
    education = forms.ChoiceField(label='Образование',
        choices=(
            ('1', 'Среднее общее'),
            ('2', 'Среднее профессиональное'),
            ('3', 'Высшее'),
        ))
    marital_status = forms.ChoiceField(label='Семейное положение',
        choices=(
            ('1', 'Замужем'),
            ('2', 'Женат'),
            ('3', 'Не женат'),
            ('4', 'Не замужем'),
            ('5', 'Разведен(-а)'),
        ))
    class Meta:
        model = TeacherInfo
        fields = ['bio', 'academic_degree', 'years_to_experience', 'date_of_employment', 'education', 'marital_status',
                  'registration_address',
                  'residential_address']
        widgets = {'bio': forms.TextInput(attrs={'placeholder': 'Введите должность преподавателя', 'class': 'form_control'}),
                   'years_to_experience': forms.TextInput(
                       attrs={'placeholder': 'Стаж работы (в годах)', 'class': 'form_control'}),
                   'date_of_employment': forms.TextInput(
                       attrs={'placeholder': 'Дата трудоустройства', 'class': 'form_control', 'type': 'date'}),
                   'registration_address': forms.TextInput(
                       attrs={'placeholder': 'Адрес по прописке (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'}),
                   'residential_address': forms.TextInput(
                       attrs={'placeholder': 'Адрес фактического проживания (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'})}


    def clean_bio(self):
        bio = self.cleaned_data["bio"]
        bio = bio[0].capitalize() + bio[1:]
        return bio

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'min_description', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Наименование курса', 'class': 'form_control'}),
            'min_description': forms.TextInput(
                attrs={'placeholder': 'Краткое описание курса', 'class': 'form_control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Подробное описание курса', 'class': 'form_control'}),
            'start_date': forms.TextInput(
                attrs={'placeholder': 'Дата начала курса', 'class': 'form_control', 'type': 'date'}),
            'end_date': forms.TextInput(
                attrs={'placeholder': 'Дата окончания курса', 'class': 'form_control', 'type': 'date'}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        title = title.upper() + title[1:]
        return title

    def clean_min_description(self):
        min_description = self.cleaned_data["min_description"]
        min_description= min_description.upper() + min_description[1:]
        return min_description

    def clean_description(self):
        description = self.cleaned_data["description"]
        description = description.upper() + description[1:]
        return description

class StudentForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', required=False, max_length=100,
                             widget=forms.EmailInput(attrs={'placeholder': 'Введите почту'}))
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'birth_date', 'pass_serial', 'pass_number', 'pass_date', 'pass_issued', 'registration_address', 'residential_address']
        widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form_control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'form_control'}),
            'birth_date': forms.DateInput(attrs={'placeholder': 'Дата рождения', 'class': 'form_control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Формат +7XXXXXXXXXX', 'class': 'form_control'}),
            'birth_date': forms.DateInput(attrs={'placeholder': 'Дата рождения', 'class': 'form_control', 'type': 'date'}),
            'pass_serial': forms.TextInput(
                       attrs={'placeholder': 'Серия паспорта (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'}),
            'pass_number': forms.TextInput(
                       attrs={'placeholder': 'Номер паспорта (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'}),
            'pass_date': forms.DateInput(
                       attrs={'placeholder': 'Дата выдачи паспорта (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control', 'type': 'date'}),
            'pass_issued': forms.TextInput(
                       attrs={'placeholder': 'Кем выдан паспорт (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'}),
            'registration_address': forms.TextInput(
                       attrs={'placeholder': 'Адрес по прописке (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'}),
            'residential_address': forms.TextInput(
                       attrs={'placeholder': 'Адрес фактического проживания (!!!НЕ НАСТОЯЩИЕ!!!)', 'class': 'form_control'})}

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        first_name = first_name.capitalize()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        last_name = last_name.capitalize()
        return last_name


    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and last_name and first_name.lower() == last_name.lower():
            self.add_error("last_name", 'Имя и фамилия не должны совпадать')


