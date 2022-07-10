from django.test import SimpleTestCase
from django.urls import reverse, resolve

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

    def test_create_category(self):
        self.assertEquals(resolve(reverse('create_category')).func.view_class, CreateCategory)

    def test_show_category_list(self):
        self.assertEquals(resolve(reverse('category', args=[1])).func.view_class, CategoryList)

    def test_journal(self):
        self.assertEquals(resolve(reverse('journal')).func.view_class, JournalView)

    def test_register(self):
        self.assertEquals(resolve(reverse('register')).func.view_class, RegisterUser)

    def test_login(self):
        self.assertEquals(resolve(reverse('login')).func.view_class, LoginUser)

    def test_logout(self):
        self.assertEquals(resolve(reverse('logout')).func.view_class, LogOut)

    def test_role_admin(self):
        self.assertEquals(resolve(reverse('rolesAdmin')).func.view_class, RegisterRoles)

    def test_create_study_material(self):
        self.assertEquals(resolve(reverse('new_study_material', args=[1])).func.view_class, CreateStudyMaterial)

    def test_display_study_material(self):
        self.assertEquals(resolve(reverse('display_study_material', args=[1])).func.view_class, DisplayStudyMaterial)

    def test_update_study_material(self):
        self.assertEquals(resolve(reverse('update_study_material', args=[1])).func.view_class, UpdateStudyMaterial)

    def test_delete_study_material(self):
        self.assertEquals(resolve(reverse('delete_study_material', args=[1])).func.view_class, DeleteStudyMaterial)

    def test_create_task(self):
        self.assertEquals(resolve(reverse('new_task', args=[1])).func.view_class, CreateTask)

    def test_display_task(self):
        self.assertEquals(resolve(reverse('display_task', args=[1])).func.view_class, DisplayTask)

    def test_delete_task(self):
        self.assertEquals(resolve(reverse('delete_task', args=[1])).func.view_class, DeleteTask)

    def test_update_task(self):
        self.assertEquals(resolve(reverse('update_task', args=[1])).func.view_class, UpdateTask)

    def test_create_test(self):
        self.assertEquals(resolve(reverse('new_test', args=[1])).func.view_class, CreateTest)

    def test_update_test(self):
        self.assertEquals(resolve(reverse('update_test', args=[1])).func.view_class, UpdateTest)

    def test_display_test(self):
        self.assertEquals(resolve(reverse('display_test', args=[1])).func.view_class, DisplayTest)

    def test_delete_test(self):
        self.assertEquals(resolve(reverse('delete_test', args=[1])).func.view_class, DeleteTest)

    def test_create_question(self):
        self.assertEquals(resolve(reverse('new_question', args=[1])).func.view_class, CreateQuestion)

    def test_update_question(self):
        self.assertEquals(resolve(reverse('update_question', args=[1, 1])).func.view_class, UpdateQuestion)

    def test_download(self):
        self.assertEquals(resolve(reverse('download')).func, download_file)

    def test_home(self):
        self.assertEquals(resolve(reverse('my_home')).func.view_class, CourseHome)