from django.test import SimpleTestCase
from django.urls import reverse, resolve
# from first_app.testdb.views import CourseHome
from testdb.views import *


class TestUrls(SimpleTestCase):
    def test_course_home_page(self):
        self.assertEquals(resolve(reverse('home')).func.view_class, CourseHome)

    def test_course_about_page(self):
        self.assertEquals(resolve(reverse('about')).func.view_class, CourseAbout)

    def test_course_list(self):
        self.assertEquals(resolve(reverse('course')).func.view_class, CourseList)

    def test_create_course(self):
        self.assertEquals(resolve(reverse('create')).func.view_class, CreateCourse)

    def test_update_course(self):
        self.assertEquals(resolve(reverse('update', args=[2])).func.view_class, UpdateCourse)

    def test_delete_course(self):
        self.assertEquals(resolve(reverse('delete', args=[1])).func.view_class, CourseDelete)

    def test_show_course(self):
        self.assertEquals(resolve(reverse('course', args=[1])).func.view_class, ShowCourse)

    def test_show_category_list(self):
        self.assertEquals(resolve(reverse('category', args=[1])).func.view_class, CategoryList)

    def test_register(self):
        self.assertEquals(resolve(reverse('register')).func.view_class, RegisterUser)

    def test_login(self):
        self.assertEquals(resolve(reverse('login')).func.view_class, LoginUser)

    def test_logout(self):
        self.assertEquals(resolve(reverse('logout')).func.view_class, LogOut)

    def test_role_admin(self):
        self.assertEquals(resolve(reverse('rolesAdmin')).func.view_class, RegisterRoles)