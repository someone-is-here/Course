from django.test import TestCase
from testdb.forms import *
from django.contrib.auth.models import User


class TestForms(TestCase):
    def test_form_admin_valid(self):
        info = {'username': 'test', 'email': 'test@domain.com', 'password': 'testpass'}
        my_user = User.objects.create_user(**info)
        my_user.save()
        form = AdminForm(data={
            'role': 'Student',
            'user': my_user
        })

        self.assertTrue(form.is_valid())

    def test_form_admin_invalid(self):
        info = {'username': 'test', 'email': 'test@domain.com', 'password': 'testpass'}
        my_user = User.objects.create_user(**info)
        my_user.save()
        form = AdminForm(data={
            'role': 'Some',
            'user': my_user
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_form_register_valid(self):
        form = RegisterForm(data={
            'username': 'test',
            'email': 'test@domain.com',
            'password1': 'testpass13',
            'password2': 'testpass13'
        })

        self.assertTrue(form.is_valid())

    def test_form_register_invalid(self):
        form = RegisterForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_form_add_course_valid(self):
        my_category = Category.objects.create(name='myCategory')
        my_category.save()
        self.assertEquals(my_category.name, 'myCategory')

        form = AddCourseForm(data={
            'title': 'myCourse',
            'description': 'Strange',
            'category': my_category.id
        })

        self.assertTrue(form.is_valid())

    def test_form_add_course_invalid(self):
        form = AddCourseForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_form_category_course_valid(self):
        form = AddCategoryForm(data={
            'name': 'myCategory',
        })

        self.assertTrue(form.is_valid())

    def test_form_category_course_invalid(self):
        form = AddCategoryForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
