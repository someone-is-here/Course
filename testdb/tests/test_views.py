from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import HttpResponse
from testdb.models import *
from testdb.views import *
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testdb/index.html')

    def test_about_GET(self):
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testdb/about.html')

    def test_course_GET(self):
        response = self.client.get(reverse('course'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testdb/course.html')

    def test_404_GET(self):
        try:
            response = self.client.get(reverse('about13'))
        except:
            response = HttpResponse(status=404)
        self.assertEquals(response.status_code, 404)

    def test_create_user(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)

        url = reverse('register')
        response = self.client.post(url, {
            'username': 'someone-is-here',
            'email': 'someone@mail.ru',
            'password1': 'TanTan139',
            'password2': 'TanTan139'
        })
        user = User.objects.get(username='someone-is-here')
        self.assertEquals(user.username, 'someone-is-here')

        res = MyAdmin.objects.get(user=user)
        self.assertEquals(res.role, 'Student')

        response = self.client.get(reverse('rolesAdmin'))
        self.assertEquals(response.status_code, 200)

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': user.id,
            'role': 'Teacher'
        })

        self.assertEquals(MyAdmin.objects.get(user=user).role, 'Teacher')

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': user.id,
            'role': 'Student'
        })

        self.assertEquals(MyAdmin.objects.get(user=user).role, 'Student')

    def test_category(self):
        my_category = Category.objects.create(name='myCategory')

        response = self.client.get(reverse('create_category'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(my_category.name, 'myCategory')

        response = self.client.get(reverse('category', args=[my_category.id]))
        self.assertEquals(response.status_code, 200)

    def test_course(self):
        info = {'username': 'test', 'email': 'test@domain.com', 'password': 'testpass13'}
        my_user = User.objects.create_user(**info)
        my_user.save()
        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': my_user.id,
            'role': 'Teacher'
        })

        self.assertEquals(MyAdmin.objects.get(user=my_user).role, 'Teacher')

        my_category = Category.objects.create(name='myCategory')
        my_category.save()
        self.assertEquals(my_category.name, 'myCategory')

        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        response = self.client.post('/create/', {
            'title': 'myCourse',
            'description': 'Strange',
            'category': my_category.id
        })

        course = Course.objects.get(title='myCourse')

        self.assertEquals(course.title, 'myCourse')
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('create'))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('update', args=[course.id]))
        self.assertEquals(response.status_code, 200)

        url = reverse('update', args=[1])

        response = self.client.post(url, {
            'title': 'MyCourse',
            'description': 'Strange',
            'category': my_category.id
        })

        course = Course.objects.get(title='MyCourse')
        self.assertEquals(course.title, 'MyCourse')
        self.assertEquals(response.status_code, 302)

        url = reverse('course', args=[1])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'testdb/selected_course.html')

        response = self.client.get(reverse('delete', args=[course.id]))
        self.assertEquals(response.status_code, 200)

        url = reverse('delete', args=[1])
        response = self.client.delete(url, json.dumps({
            'id': 1
        }))

        self.assertEquals(Course.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_study_material(self):
        info = {'username': 'test', 'email': 'test@domain.com', 'password': 'testpass13'}
        my_user = User.objects.create_user(**info)
        my_user.save()
        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': my_user.id,
            'role': 'Teacher'
        })

        self.assertEquals(MyAdmin.objects.get(user=my_user).role, 'Teacher')

        my_category = Category.objects.create(name='myCategory')
        my_category.save()
        self.assertEquals(my_category.name, 'myCategory')

        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        Course.objects.create(title='myCourse', description='Strange', category=my_category)
        course = Course.objects.get(title='myCourse')

        response = self.client.post(f'/createStudyMaterial/{course.id}/', {
            'title': 'myStudyMaterial',
            'description': 'MyStudyMaterialDescription',
            'material': 'Something important',
            'picture': '/home/tanusha/Documents/Python_Labs_2-/python_lab3/first_app/htmlcov/favicon_32.png'
        })

        study_material = StudyMaterial.objects.get(title='myStudyMaterial')

        self.assertEquals(study_material.description, 'MyStudyMaterialDescription')
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('new_study_material', args=[course.id]))
        self.assertEquals(response.status_code, 200)

        url = reverse('display_study_material', args=[study_material.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('update_study_material', args=[study_material.pk]))
        self.assertEquals(response.status_code, 200)

        url = reverse('update_study_material', args=[study_material.pk])

        response = self.client.post(url, {
            'title': 'MyStudyMaterial',
            'description': 'MyStudyMaterialDescription',
            'material': 'Something important'
        })

        updated_study_material = StudyMaterial.objects.get(title='MyStudyMaterial')
        self.assertEquals(updated_study_material.title, 'MyStudyMaterial')
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('delete_study_material', args=[study_material.pk]))
        self.assertEquals(response.status_code, 200)

        url = reverse('delete_study_material', args=[1])
        response = self.client.delete(url, json.dumps({
            'id': 1
        }))

        self.assertEquals(StudyMaterial.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_task(self):
        info = {'username': 'test', 'email': 'test@domain.com', 'password': 'testpass13'}
        my_user = User.objects.create_user(**info)
        my_user.save()
        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': my_user.id,
            'role': 'Teacher'
        })

        self.assertEquals(MyAdmin.objects.get(user=my_user).role, 'Teacher')

        my_category = Category.objects.create(name='myCategory')
        my_category.save()
        self.assertEquals(my_category.name, 'myCategory')

        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        Course.objects.create(title='myCourse', description='Strange', category=my_category)
        course = Course.objects.get(title='myCourse')

        response = self.client.post(f'/createTask/{course.id}/', {
            'title': 'myTask',
            'task': '3*8',
            'result': '24',
            'mark': '2'
        })

        task = Task.objects.get(title='myTask')

        self.assertEquals(task.task, '3*8')
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('new_task', args=[course.id]))
        self.assertEquals(response.status_code, 200)

        url = reverse('display_task', args=[task.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        url = reverse('update_task', args=[task.pk])

        response = self.client.post(url, {
            'title': 'myTask',
            'task': '3*8',
            'result': '24',
            'mark': '3'
        })

        updated_task = Task.objects.get(title='myTask')
        self.assertEquals(updated_task.mark, 3)
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('update_task', args=[task.pk]))
        self.assertEquals(response.status_code, 200)

        info1 = {'username': 'test_student', 'email': 'test_studnt@domain.com', 'password': 'testpass123'}
        my_user_student = User.objects.create_user(**info1)
        my_user_student.save()
        response = self.client.post('/login/', info1)
        self.assertEquals(response.status_code, 302)

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': my_user_student.id,
            'role': 'Student'
        })

        self.assertEquals(MyAdmin.objects.get(user=my_user_student).role, 'Student')

        url = reverse('display_task', args=[task.pk])
        response = self.client.post(url, {
            'answer': '24'
        })
        response = self.client.post(url, {
            'answer': '25'
        })
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('delete_task', args=[task.pk]))
        self.assertEquals(response.status_code, 200)

        url = reverse('delete_task', args=[1])
        response = self.client.delete(url, json.dumps({
            'id': 1
        }))

        self.assertEquals(Task.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_test(self):
        info = {'username': 'test', 'email': 'test@domain.com', 'password': 'testpass13'}
        my_user = User.objects.create_user(**info)
        my_user.save()
        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': my_user.id,
            'role': 'Teacher'
        })

        self.assertEquals(MyAdmin.objects.get(user=my_user).role, 'Teacher')

        my_category = Category.objects.create(name='myCategory')
        my_category.save()
        self.assertEquals(my_category.name, 'myCategory')

        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        Course.objects.create(title='myCourse', description='Strange', category=my_category)
        course = Course.objects.get(title='myCourse')

        response = self.client.get(reverse('new_test', args=[course.pk]))
        self.assertEquals(response.status_code, 200)

        response = self.client.post(f'/createTest/{course.id}/', {
            'title': 'myTest',
        })

        test = CourseTest.objects.get(title='myTest')

        self.assertEquals(test.title, 'myTest')
        self.assertEquals(response.status_code, 302)

        url = reverse('display_test', args=[test.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('update_test', args=[test.pk]))
        self.assertEquals(response.status_code, 200)

        url = reverse('update_test', args=[test.pk])

        response = self.client.post(url, {
            'title': 'MyNewTest',
        })

        updated_test = CourseTest.objects.get(title='MyNewTest')
        self.assertEquals(updated_test.title, 'MyNewTest')
        self.assertEquals(response.status_code, 302)

        # response = self.client.post('/login/', info)
        # self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('delete_test', args=[test.pk]))
        self.assertEquals(response.status_code, 200)

        url = reverse('delete_test', args=[test.pk])
        response = self.client.delete(url, json.dumps({
            'id': 1
        }))

        self.assertEquals(CourseTest.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    # def test_test_question(self):
    #     response = self.client.get(f'/createQuestion/1/', {
    #         'title': 'myTest',
    #     })
    #
    #     test = CourseTest.objects.get(title='myTest')
    #
    #     self.assertEquals(test.title, 'myTest')
    #     self.assertEquals(response.status_code, 302)
    #
    #     # response = self.client.post(f'/createQuestion/1/', {
    #     #     'title': 'myTest',
    #     # })

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_category_create(self):
        info1 = {'username': 'test_student', 'email': 'test_studnt@domain.com', 'password': 'testpass123'}
        my_user_student = User.objects.create_user(**info1)
        my_user_student.save()
        response = self.client.post('/login/', info1)
        self.assertEquals(response.status_code, 302)

        url = reverse('rolesAdmin')
        response = self.client.post(url, {
            'user': my_user_student.id,
            'role': 'Student'
        })

        self.assertEquals(MyAdmin.objects.get(user=my_user_student).role, 'Student')

        response = self.client.get(reverse('create_category'))
        self.assertEquals(response.status_code, 200)

        url = reverse('create_category')

        response = self.client.post(url, {
            'name': 'myCategory',
        })

        course = Category.objects.get(name='myCategory')
        self.assertEquals(course.name, 'myCategory')
        self.assertEquals(response.status_code, 302)

