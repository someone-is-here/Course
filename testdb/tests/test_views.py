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
            return HttpResponse(status=404)
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, 'testdb/404.html')

    def test_create_user(self):
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

    def test_category(self):
        my_category = Category.objects.create(name='myCategory')
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

        url = reverse('delete', args=[1])
        response = self.client.delete(url, json.dumps({
            'id': 1
        }))

        self.assertEquals(Course.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_category_create(self):
        info = {'username': 'test', 'email': 'test@domain.com', 'password': 'testpass13'}
        my_user = User.objects.create_user(**info)
        my_user.save()
        response = self.client.post('/login/', info)
        self.assertEquals(response.status_code, 302)

        url = reverse('create_category')

        response = self.client.post(url, {
            'name': 'myCategory',
        })

        course = Category.objects.get(name='myCategory')
        self.assertEquals(course.name, 'myCategory')
        self.assertEquals(response.status_code, 302)
