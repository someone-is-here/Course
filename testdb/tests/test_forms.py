from django.test import TestCase
from testdb.forms import *


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

    def test_form_add_study_material_valid(self):
        form = AddStudyMaterialForm(data={
            'title': 'Study material',
            'description': 'My study material',
            'material': 'Useful information',
        })

        self.assertTrue(form.is_valid())

    def test_form_add_study_material_invalid(self):
        form = AddStudyMaterialForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_form_add_task(self):
        form = AddTaskForm(data={
            'title': 'Solve the task',
            'task': '3*7',
            'result': '21',
            'mark': '1'
        })

        self.assertTrue(form.is_valid())

    def test_form_add_task_invalid(self):
        form = AddTaskForm(data={
            'title': 'Solve the task',
            'task': '3*7',
            'result': '21',
            'mark': '-1'})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_form_add_task_invalid_all(self):
        form = AddTaskForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_form_add_test(self):
        form = AddCourseTestForm(data={
            'title': 'Result test'
        })

        self.assertTrue(form.is_valid())

    def test_form_add_test_invalid(self):
        form = AddCourseTestForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_form_add_test_question(self):
        form = AddTestQuestionForm(data={
            'question': 'How many days are in week?',
            'score': 1,
        })

        self.assertTrue(form.is_valid())

    def test_form_add_test_question_invalid(self):
        form = AddTestQuestionForm(data={
            'question': 'How many days are in week?',
            'score': -45,
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_form_add_test_question_invalid_all(self):
        form = AddTestQuestionForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_form_add_test_answers(self):
        form = AddTestAnswerForm(data={
            'answer': '7',
            'is_right': True,
        })

        self.assertTrue(form.is_valid())

    def test_form_add_test_answers_invalid(self):
        form = AddTestAnswerForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
