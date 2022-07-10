
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *


urlpatterns = [
    path("", CourseHome.as_view(), name="my_home"),
    path("home/", CourseHome.as_view(), name="home"),
    path("about/", CourseAbout.as_view(), name="about"),
    path("course/", CourseList.as_view(), name="course"),
    path("create/", CreateCourse.as_view(), name="create"),
    path("update/<int:course_id>/", UpdateCourse.as_view(), name="update"),
    path("delete/<int:course_id>/", CourseDelete.as_view(), name="delete"),
    path('course/<int:course_id>/', ShowCourse.as_view(), name='course'),
    path('category/<int:category_id>/', CategoryList.as_view(), name='category'),
    path('createCategory/', CreateCategory.as_view(), name='create_category'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('journal/', JournalView.as_view(), name='journal'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('rolesAdmin/', RegisterRoles.as_view(), name='rolesAdmin'),
    path('createStudyMaterial/<int:course_id>/', CreateStudyMaterial.as_view(), name='new_study_material'),
    path('displayStudyMaterial/<int:study_material_id>/', DisplayStudyMaterial.as_view(), name='display_study_material'),
    path('updateStudyMaterial/<int:study_material_id>/', UpdateStudyMaterial.as_view(), name='update_study_material'),
    path('deleteStudyMaterial/<int:study_material_id>/', DeleteStudyMaterial.as_view(), name='delete_study_material'),
    path('createTask/<int:course_id>/', CreateTask.as_view(), name='new_task'),
    path('displayTask/<int:task_id>/', DisplayTask.as_view(), name='display_task'),
    path('deleteTask/<int:task_id>/', DeleteTask.as_view(), name='delete_task'),
    path('updateTask/<int:task_id>/', UpdateTask.as_view(), name='update_task'),
    path('createTest/<int:course_id>/', CreateTest.as_view(), name='new_test'),
    path('updateTest/<int:test_id>/', UpdateTest.as_view(), name='update_test'),
    path('displayTest/<int:test_id>/', DisplayTest.as_view(), name='display_test'),
    path('deleteTest/<int:test_id>/', DeleteTest.as_view(), name='delete_test'),
    path('createQuestion/<int:test_id>/', CreateQuestion.as_view(), name='new_question'),
    path('updateQuestion/<int:test_id>/<int:question_id>/', UpdateQuestion.as_view(), name='update_question'),
    path('download/', views.download_file, name='download'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
