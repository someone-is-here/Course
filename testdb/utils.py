from .models import *
from django.db.models import Count, Q
import logging


menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'Courses', 'url_name': 'course'},
        {'title': 'About', 'url_name': 'about'}]

teachers_menu = [{'title': 'Home', 'url_name': 'home'},
                 {'title': 'Courses', 'url_name': 'course'},
                 {'title': 'About', 'url_name': 'about'},
                 {'title': 'Add Course', 'url_name': 'create'},
                 {'title': 'Add category', 'url_name': 'create_category'},
                 {'title': 'Roles', 'url_name': 'rolesAdmin'}]

student_menu = menu + [{'title': 'Journal', 'url_name': 'journal'}]

logger = logging.getLogger('main')


class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        context['my_user'] = self.request.user

        if self.request.user.is_authenticated and MyAdmin.objects.get(user=self.request.user).role == 'Teacher':
            context['menu'] = teachers_menu
            context['teacher'] = 1
        elif self.request.user.is_authenticated and MyAdmin.objects.get(user=self.request.user).role == 'Student':
            context['menu'] = student_menu
            context['teacher'] = 0
        else:
            context['menu'] = menu
            context['teacher'] = 0

        category_info = Category.objects.annotate(amount=Count('course')).filter(amount__gt=0)

        for item in category_info:
            res = Course.objects.filter(category_id=item.id, is_working=True).count()
            item.amount = res

        context['categories'] = category_info

        if 'category_selected' not in context:
            context['category_selected'] = 0

        logger.info('get_context. class: DataMixin')

        return context
