from django.contrib import admin
from .models import *

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'time_create', 'time_update', 'icon', 'is_working')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('is_working', )
    list_filter = ('time_create', 'is_working', 'time_update')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'picture', 'files')
    list_display_links = ('id', 'title', 'description', 'picture', 'files')
    search_fields = ('title',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'task', 'picture', 'result', 'mark')
    list_display_links = ('id', 'title', 'task', 'picture', 'result', 'mark')
    search_fields = ('title',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'score', 'course')
    list_display_links = ('id', 'title', 'score','course')
    search_fields = ('title',)


class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'score', 'test', 'test_picture')
    list_display_links = ('id', 'question', 'score', 'test', 'test_picture')
    search_fields = ('question',)


class TestAnswersAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'is_right', 'question')
    list_display_links = ('id', 'answer', 'is_right', 'question')
    search_fields = ('title',)


class JournalTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'mark', 'test')
    list_display_links = ('id', 'student', 'mark', 'test')


class JournalTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'mark', 'task')
    list_display_links = ('id', 'student', 'mark', 'task')


class MyAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    list_display_links = ('id', 'user', 'role')


admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(StudyMaterial, StudyMaterialAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(CourseTest, TestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(TestAnswer, TestAnswersAdmin)
admin.site.register(MyAdmin, MyAdminAdmin)
admin.site.register(JournalTask, JournalTaskAdmin)
admin.site.register(JournalTest, JournalTestAdmin)
