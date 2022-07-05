from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import *


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True) #индексированное поле

    class Meta:
        verbose_name_plural = 'All categories'
        verbose_name = 'Category'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to="icons/%Y/%m/%d/", blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_working = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name_plural = 'All courses'
        verbose_name = 'Course'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', kwargs={'course_id': self.pk})


class StudyMaterial(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    picture = models.ImageField(upload_to="icons/study_materials_pictures/%Y/%m/%d/", blank=True, null=True)
    material = models.TextField()

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'All materials'
        verbose_name = 'Study materials'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('display_study_material', kwargs={'study_material_id': self.pk})


class Task(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="icons/task_pictures/%Y/%m/%d/", blank=True, null=True)
    task = models.TextField()
    result = models.TextField()
    mark = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Tasks'
        verbose_name = 'Tasks'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('display_task', kwargs={'task_id': self.pk})


class CourseTest(models.Model):
    title = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('display_test', kwargs={'test_id': self.pk})


class JournalTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    test = models.ForeignKey(CourseTest, on_delete=models.DO_NOTHING)


class JournalTask(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)


class TestQuestion(models.Model):
    question = models.CharField(max_length=200)
    test = models.ForeignKey(CourseTest, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=1)
    test_picture = models.ImageField(upload_to="icons/test_pictures/%Y/%m/%d/", blank=True, null=True)

    def __str__(self):
        return self.question


class TestAnswer(models.Model):
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, null=True)
    is_right = models.BooleanField(default=False)


class MyAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Roles(models.TextChoices):
        STUDENT = 'Student', _('Student')
        TEACHER = 'Teacher', _('Teacher')

    role = models.CharField(
        max_length=15,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )

    @staticmethod
    def get_absolute_url():
        return reverse('rolesAdmin')
