from django import forms
from django.forms import formset_factory

from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AddCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Choose category'

    class Meta:
        model = Course
        fields = ['title', 'description', 'icon', 'is_working', 'category']
        widgets = {
            'title': forms.TimeInput(attrs={'class': 'forms-input'}),
            'description': forms.TimeInput(attrs={'class': 'forms-input'})
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username:", widget=forms.TextInput)
    email = forms.EmailField(label="Email:", widget=forms.EmailInput)

    password1 = forms.CharField(label="Password:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AdminForm(forms.ModelForm):
    class Meta:
        model = MyAdmin
        fields = ['user', 'role']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'task',  'picture', 'result', 'mark']


class AddStudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'material', 'picture', 'files']


class AddCourseTestForm(forms.ModelForm):
    class Meta:
        model = CourseTest
        fields = ['title']


class AddTestQuestionForm(forms.ModelForm):
    class Meta:
        model = TestQuestion
        fields = ['question', 'score', 'test_picture']


class AddTestAnswerForm(forms.ModelForm):
    class Meta:
        model = TestAnswer
        fields = ['answer', 'is_right']


QuestionsFormSet = formset_factory(AddTestAnswerForm, extra=4)
