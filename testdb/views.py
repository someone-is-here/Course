import asyncio.coroutines
import mimetypes
import os

from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import *
from .forms import *
from django.urls import reverse_lazy
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
import logging
from django.db.models import Sum
from django.utils.decorators import classonlymethod
from asgiref.sync import sync_to_async

logger = logging.getLogger('main')


class CourseHome(DataMixin, View):
    def get(self, request, *args, **kwargs):
        context = DataMixin.get_user_context(self)
        logger.info('To index.html page. class: CourseHome')
        return render(request, 'testdb/index.html', context=context)


class CourseList(DataMixin, ListView):
    model = Course
    template_name = "testdb/course.html"
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        if self.request.user.is_authenticated and MyAdmin.objects.get(user=self.request.user).role == 'Teacher':
            context2['teacher'] = 1
        else:
            context2['teacher'] = 0

        return dict(list(context2.items()) + list(context.items()))

    def get_queryset(self):
        logger.info('Query, class: CourseList')

        return Course.objects.filter(is_working=True)


class CourseAbout(View):
    def get(self, request, *args, **kwargs):
        context = DataMixin.get_user_context(self)
        logger.info('To about.html, class: CourseAbout')

        return render(request, 'testdb/about.html', context=context)


class CreateCourse(LoginRequiredMixin, CreateView):
    form_class = AddCourseForm
    template_name = "testdb/create.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context['title'] = 'Creating course'
        context['my_url'] = 'create'

        return dict(list(context2.items()) + list(context.items()))


class CreateCategory(LoginRequiredMixin, CreateView):
    form_class = AddCategoryForm
    template_name = "testdb/create_category.html"
    success_url = reverse_lazy('course')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        return dict(list(context2.items()) + list(context.items()))


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = AddTaskForm
    pk_url_kwarg = 'course_id'
    template_name = "testdb/create.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context['title'] = 'Creating task'
        context['my_url'] = 'new_task'
        context['course_id'] = self.kwargs['course_id']

        return dict(list(context2.items()) + list(context.items()))

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.kwargs['course_id'])
        form.save()

        logger.info(f'To display_task.html({form.instance.pk}) page. class: CreateTask')

        return HttpResponseRedirect(reverse('display_task', args=[form.instance.pk]))


class CreateStudyMaterial(LoginRequiredMixin, CreateView):
    form_class = AddStudyMaterialForm
    template_name = "testdb/create.html"
    pk_url_kwarg = 'course_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context['title'] = 'Creating study material'
        context['my_url'] = 'new_study_material'
        context['course_id'] = self.kwargs['course_id']

        return dict(list(context2.items()) + list(context.items()))

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.kwargs['course_id'])
        form.save()

        logger.info(f'To display_study_material.html({form.instance.pk}) page. class: CreateStudyMaterial')

        return HttpResponseRedirect(reverse('display_study_material', args=[form.instance.pk]))


class ShowCourse(DetailView):
    model = Course
    template_name = "testdb/selected_course.html"
    pk_url_kwarg = 'course_id'
    context_object_name = 'course_info'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        context2['study_material'] = StudyMaterial.objects.select_related('course').filter(
            course_id=self.kwargs['course_id'])
        context2['task'] = Task.objects.prefetch_related('course').filter(course_id=self.kwargs['course_id'])
        context2['test'] = CourseTest.objects.prefetch_related('course').filter(course_id=self.kwargs['course_id'])

        logger.info('Load study_materials, tests and tasks from db. class: ShowCourse')

        return dict(list(context2.items()) + list(context.items()))


class DisplayStudyMaterial(DetailView):
    model = StudyMaterial
    template_name = "testdb/study_material.html"
    pk_url_kwarg = 'study_material_id'
    context_object_name = 'study_material_info'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        return dict(list(context2.items()) + list(context.items()))


class DisplayTask(TemplateView):
    template_name = "testdb/task.html"
    my_context = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        self.my_context = dict(list(context2.items()) + list(context.items()))

        self.my_context['task_info'] = Task.objects.get(pk=self.kwargs['task_id'])

        if JournalTask.objects.filter(task=Task.objects.get(pk=self.kwargs['task_id'])).exists():
            self.my_context['message'] = "Task already solved!"

        logger.info(f'Load task_info from db, is_solved from journal_task. class: DisplayTask')

        return self.my_context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        self.my_context = context

        logger.info(f'To testdb/task.html. class: DisplayTask')

        return self.render_to_response(context=self.my_context)

    def post(self, request, task_id):
        self.get_context_data()
        data = request.POST
        task_res = Task.objects.get(pk=task_id)

        if task_res.result == data['answer']:
            self.my_context['message'] = "Right! Excellent job!"
            if not JournalTask.objects.filter(task=Task.objects.get(pk=task_id)).exists():
                JournalTask.objects.create(student=self.request.user, mark=task_res.mark, task=Task.objects.get(pk=task_id))
        else:
            self.my_context['message'] = "Wrong answer! Try again!"
        self.my_context['task_info'] = Task.objects.get(pk=task_id)

        logger.info('POST from testdb/task.html. class: DisplayTask')

        return self.render_to_response(context=self.my_context)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'task', 'picture', 'result', 'mark']
    template_name = "testdb/update.html"
    pk_url_kwarg = 'task_id'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context2['title'] = 'Update task'

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        logger.info('Task updated successfully. class: UpdateTask')

        return reverse('display_task', args=[self.kwargs['task_id']])


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('/')
    template_name = "testdb/delete.html"
    pk_url_kwarg = 'task_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context2['title'] = 'Delete task'

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        task_material = Task.objects.filter(pk=self.kwargs['task_id']).get()

        logger.info('Delete task from testdb/delete.html. class: DeleteTask')

        return reverse('course', args=[task_material.course.id])


def download_file(request, filename=''):
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/filedownload/Files/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'file.html')


class UpdateStudyMaterial(LoginRequiredMixin, UpdateView):
    model = StudyMaterial
    fields = ['title', 'description', 'material', 'picture', 'files']
    template_name = "testdb/update.html"
    pk_url_kwarg = 'study_material_id'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context2['title'] = 'Update study material'

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        logger.info('Study material updated successfully. class: UpdateStudyMaterial')

        return reverse('display_study_material', args=[self.kwargs['study_material_id']])


class DeleteStudyMaterial(LoginRequiredMixin, DeleteView):
    model = StudyMaterial
    template_name = "testdb/delete.html"
    pk_url_kwarg = 'study_material_id'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context2['title'] = 'Delete study material'

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        st_material = StudyMaterial.objects.filter(pk=self.kwargs['study_material_id']).get()

        logger.info('Delete study_material from testdb/delete.html. class: DeleteStudyMaterial')

        return reverse('course', args=[st_material.course.id])


class CategoryList(ListView):
    model = Course
    template_name = "testdb/course.html"
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self, **{'category_id': self.kwargs['category_id']})

        return dict(list(context2.items()) + list(context.items()))

    def get_queryset(self):
        logger.info('Query, class: CategoryList')

        return Course.objects.filter(category_id=self.kwargs['category_id'], is_working=True)


class UpdateCourse(LoginRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'description', 'icon', 'is_working']
    template_name = "testdb/update.html"
    pk_url_kwarg = 'course_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context['title'] = 'Updating course'

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        logger.info('Course updated successfully. class: UpdateCourse')

        return reverse('course', args=[self.kwargs['course_id']])


class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('course')
    template_name = "testdb/delete.html"
    pk_url_kwarg = 'course_id'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context2['title'] = 'Delete course'

        return dict(list(context2.items()) + list(context.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'testdb/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        return dict(list(context2.items()) + list(context.items()))

    def form_valid(self, form):
        user = form.save()
        MyAdmin.objects.create(role=MyAdmin.Roles.STUDENT, user=user)
        user.save()

        logger.info('Create user, class: RegisterUser')
        login(self.request, user)
        logger.info('Login user, class: RegisterUser')

        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'testdb/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        logger.info('Login user. Redirect to home, class: LoginUser')

        return reverse_lazy('home')


class LogOut(DataMixin, View):
    def get(self, request):
        logout(request)
        logger.info('Logout. Redirect to login, class: LogOut')
        return redirect('login')


class RegisterRoles(DataMixin, CreateView):
    form_class = AdminForm
    template_name = 'testdb/admin.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        return dict(list(context2.items()) + list(context.items()))

    def form_valid(self, form):
        form.save()

        logger.info('Redirect to rolesAdmin, class: RegisterRoles')

        return redirect('rolesAdmin')

    def form_invalid(self, form):
        role = form['role'].value()
        user = form['user'].value()
        res = MyAdmin.objects.select_related('user').filter(user=user).get()
        res.role = role
        res.save()

        logger.info('Update role. Redirect to rolesAdmin, class: RegisterRoles')

        return redirect('rolesAdmin')


class CreateTest(LoginRequiredMixin, CreateView):
    form_class = AddCourseTestForm
    template_name = "testdb/create.html"
    success_url = '/'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        context['title'] = 'Creating test'

        context['my_url'] = 'new_test'
        context['course_id'] = self.kwargs['course_id']

        return dict(list(context2.items()) + list(context.items()))

    def form_valid(self, form, **kwargs):
        form.instance.course = Course.objects.get(pk=self.kwargs['course_id'])
        form.save()

        logger.info('Test created successfully. Redirect to display_test, class: CreateTest')

        return HttpResponseRedirect(reverse('display_test', args=[form.instance.pk]))


class UpdateTest(LoginRequiredMixin, UpdateView):
    model = CourseTest
    fields = ['title']
    template_name = "testdb/update.html"
    pk_url_kwarg = 'test_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context['title'] = 'Updating test'

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        logger.info('Test updated successfully. Redirect to display_test, class: UpdateTest')

        return reverse('display_test', args=[self.kwargs['test_id']])


def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)


class DisplayTest(TemplateView):
    template_name = 'testdb/test.html'
    my_context = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)

        query_set_test = TestQuestion.objects.filter(test=self.kwargs['test_id'])

        context2['questions'] = query_set_test
        context2['quest_ans'] = []

        for i in range(len(query_set_test)):
            context2['quest_ans'].append({})
            context2['quest_ans'][i]['questions'] = query_set_test[i]

        res = TestQuestion.objects.filter(test=self.kwargs['test_id']).aggregate(Sum('score'))

        if res['score__sum']:
            CourseTest.objects.filter(id=self.kwargs['test_id']).update(score=res['score__sum'])
        else:
            CourseTest.objects.filter(id=self.kwargs['test_id']).update(score=0)
            context['no_questions'] = True

        context['test_info'] = CourseTest.objects.get(pk=self.kwargs['test_id'])

        for i in range(len(query_set_test)):
            item = query_set_test[i]
            context2['quest_ans'][i]['answers'] = list(TestAnswer.objects.filter(question_id=item.pk))

        if JournalTest.objects.filter(test=CourseTest.objects.get(pk=self.kwargs['test_id'])).exists():
            context2['message'] = "Test already solved!"

        self.my_context = dict(list(context2.items()) + list(context.items()))

        logger.info('Get all info for displaying test. class: DisplayTest')

        return self.my_context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        self.my_context = context

        logger.info('GET Render testdb/test.html, class: DisplayTest')

        return self.render_to_response(context=self.my_context)

    def post(self, request, test_id):
        self.get_context_data()
        save_form_res = request.POST
        data = save_form_res.copy()

        logger.info('POST from testdb/test.html , class: DisplayTest')

        score_res = 0
        query_set_test = TestQuestion.objects.filter(test=self.kwargs['test_id'])
        k = 0

        while k < len(query_set_test):
            answers = []

            for item in list(data.items()):
                key = item[0]

                if key.__contains__('_') and query_set_test[k].id == int(key[:key.index('_')]):
                    data.pop(key)
                    answers.append(int(key[(key.index('_') + 1):]))

            ans_from_db = TestAnswer.objects.filter(question_id=query_set_test[k].id, is_right=True)

            wrong = False
            if len(ans_from_db) == len(answers):
                for i in range(len(ans_from_db)):
                    if answers.__contains__(ans_from_db[i].pk):
                        answers.remove(ans_from_db[i].pk)
                    else:
                        wrong = True
                if not wrong:
                    score_res += query_set_test[k].score
            k += 1

        if JournalTest.objects.filter(test=CourseTest.objects.get(pk=self.kwargs['test_id'])).exists():
            self.my_context['message'] = f"Test already solved! Your result is {score_res}/" \
                                         f"{CourseTest.objects.get(pk=self.kwargs['test_id']).score}!"

        if not JournalTest.objects.filter(test=CourseTest.objects.get(pk=test_id)).exists():
            JournalTest.objects.create(student=self.request.user, mark=score_res,
                                       test=CourseTest.objects.get(pk=test_id))
            self.my_context['message'] = f"Excellent job!\nYour result is {score_res}/" \
                                         f"{CourseTest.objects.get(pk=self.kwargs['test_id']).score}"

        logger.info('Render_to_response to testdb/test.html , class: DisplayTest')

        return self.render_to_response(context=self.my_context)


class DeleteTest(LoginRequiredMixin, DeleteView):
    model = CourseTest
    template_name = "testdb/delete.html"
    pk_url_kwarg = 'test_id'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = DataMixin.get_user_context(self)
        context2['title'] = 'Delete test'

        return dict(list(context2.items()) + list(context.items()))

    def get_success_url(self):
        test = CourseTest.objects.filter(pk=self.kwargs['test_id']).get()

        logger.info('Return to course, test deleted successfully. class: DeleteTest')

        return reverse('course', args=[test.course.id])


async def page_not_found_view(request, exception):
    logger.error("Page not found. Error 404")

    return render(request, 'testdb/404.html', status=404)


async def page405(request, exception):
    logger.error("Page not found. Error 405")

    return render(request, 'testdb/405.html', status=405)


def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None

    return formcls(data, request.FILES, prefix=prefix)


class CreateQuestion(TemplateView):
    template_name = 'testdb/question.html'
    my_context = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        context2 = DataMixin.get_user_context(self)
        context['title'] = 'Creating questions'

        return dict(list(context2.items()) + list(context.items()))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['aform'] = AddTestQuestionForm(prefix='aform_pre')
        context['bform'] = QuestionsFormSet(prefix='bform_pre')

        self.my_context = context

        logger.info('GET testdb/question.html, created forms. class: CreateQuestion')

        return self.render_to_response(context=self.my_context)

    def post(self, request, *args, **kwargs):
        aform = _get_form(request, AddTestQuestionForm, 'aform_pre')
        bform = _get_form(request, QuestionsFormSet, 'bform_pre')

        context = self.get_context_data()
        context['aform'] = aform
        context['bform'] = bform
        context['error_messages'] = []

        if bform.is_bound and bform.is_valid() and aform.is_valid():
            is_right_cont = False

            for form in bform:
                if form.instance.is_right:
                    is_right_cont = True

            if is_right_cont:
                aform.instance.test = CourseTest.objects.get(pk=kwargs['test_id'])

                if bform.is_valid():
                    a_form = aform.save()

                    for form in bform:
                        if len(str(form.instance.answer)) == 0:
                            continue

                        form.instance.question = TestQuestion.objects.get(pk=a_form.pk)
                        form.save()

                logger.info('POST testdb/question.html, created successfully. class: CreateQuestion')

                return HttpResponseRedirect(reverse('display_test', args=[kwargs['test_id']]))

            else:
                context['error_messages'].append("Must be at least one right answer!")

        logger.info('POST testdb/question.html render_to_response. class: CreateQuestion')

        return self.render_to_response(context=context)


class UpdateQuestion(TemplateView):
    template_name = 'testdb/question.html'
    my_context = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        context2 = DataMixin.get_user_context(self)
        context['title'] = 'Update questions'

        return dict(list(context2.items()) + list(context.items()))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        test_question = TestQuestion.objects.get(pk=self.kwargs['question_id'])
        test_answers = TestAnswer.objects.filter(question=self.kwargs['question_id']).order_by('pk')

        context['aform'] = AddTestQuestionForm(initial={'question': test_question.question,
                                                        'score': test_question.score,
                                                        'test_picture': test_question.test_picture},
                                               prefix='aform_pre')

        question_formset = QuestionsFormSet(prefix='bform_pre')
        i = 0

        for item in question_formset:
            item.initial = {'answer': test_answers[i].answer, 'is_right': test_answers[i].is_right}
            i += 1
            if i == len(test_answers):
                break

        context['bform'] = question_formset

        self.my_context = context

        logger.info('GET testdb/question.html. class: UpdateQuestion')

        return self.render_to_response(context=self.my_context)

    def post(self, request, *args, **kwargs):
        aform = _get_form(request, AddTestQuestionForm, 'aform_pre')
        bform = _get_form(request, QuestionsFormSet, 'bform_pre')

        context = self.get_context_data()
        context['aform'] = aform
        context['bform'] = bform
        context['error_messages'] = []

        if bform.is_bound and bform.is_valid() and aform.is_valid():
            is_right_cont = False

            for form in bform:
                if form.instance.is_right:
                    is_right_cont = True
                    break

            if is_right_cont:
                test_question = TestQuestion.objects.get(pk=self.kwargs['question_id'])
                test_answers = TestAnswer.objects.filter(question=self.kwargs['question_id']).order_by('pk')

                test_question.question = aform.instance.question
                test_question.score = aform.instance.score
                test_question.test_picture = aform.instance.test_picture
                test_question.save()

                i = 0
                for form in bform:
                    if i < len(test_answers):
                        ans = TestAnswer.objects.get(pk=test_answers[i].pk)

                        if len(str(form.instance.answer)) > 0:
                            ans.answer = form.instance.answer
                            ans.is_right = form.instance.is_right

                            ans.save()
                        else:
                            ans.delete()
                    else:
                        TestAnswer.objects.create(answer=form.instance.answer,
                                                  is_right=form.instance.is_right,
                                                  question=test_question)

                    i += 1

                logger.info('POST testdb/question.html, updated successfully. class: UpdateQuestion')

                return HttpResponseRedirect(reverse('display_test', args=[kwargs['test_id']]))

            else:
                context['error_messages'].append("Must be at least one right answer!")

        logger.info('POST testdb/question.html, updated unsuccessfully. class: UpdateQuestion')

        return self.render_to_response(context=context)


class JournalView(DataMixin, View):
    def get(self, request, *args, **kwargs):
        context = DataMixin.get_user_context(self)

        logger.info('To journal.html page. class: JournalView')

        courses = Course.objects.filter(is_working=True)
        context['course'] = []

        for i in range(len(courses)):
            context['course'].append({})

            context['course'][i]['name'] = courses[i].title
            context['course'][i]['link'] = reverse('course', args=[courses[i].id])
            context['course'][i]['tasks'] = []
            context['course'][i]['tests'] = []

            tasks = Task.objects.filter(course=courses[i])
            tests = CourseTest.objects.filter(course=courses[i])

            if len(tasks) > 0:
                k = 0

                for task in list(tasks):
                    context['course'][i]['tasks'].append({})
                    task_res = JournalTask.objects.filter(student=self.request.user, task=task)

                    if len(task_res) > 0:
                        context['course'][i]['tasks'][k]['task_content'] = task
                        context['course'][i]['tasks'][k]['task_result'] = task_res[0].mark
                    else:
                        context['course'][i]['tasks'][k]['task_content'] = task

                    k += 1

            if len(tests) > 0:
                k = 0

                for test in list(tests):
                    context['course'][i]['tests'].append({})
                    test_res = JournalTest.objects.filter(student=self.request.user, test=test)

                    if len(test_res) > 0:
                        context['course'][i]['tests'][k]['test_content'] = test
                        context['course'][i]['tests'][k]['test_result'] = test_res[0].mark
                    elif test.score > 0:
                        context['course'][i]['tests'][k]['test_content'] = test

                    k += 1

        return render(request, 'testdb/journal.html', context=context)
