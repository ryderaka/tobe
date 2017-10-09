# -*- coding: utf-8 -*-

from tobe.models import TodoList, TodoUser
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.core.paginator import Paginator

# from tobe.serializer import TodoTaskSerializer


class Tasks:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def create_task(self, receiver, title, description, assigned_date, due_date):
        task = TodoList(title=title, description=description,
                        created_by=TodoUser.objects.get(auth_token=self.auth_token),
                        assigned_to=TodoUser.objects.get(phone=receiver),
                        assigned_date=assigned_date, due_date=due_date)
        try:
            task.save()
            return True
        except:
            return False

    def dashboard(self, view_type=None, page_num=None):
        try:
            user = TodoUser.objects.get(auth_token=self.auth_token)

            if view_type == 'today':
                today_start = datetime.combine(datetime.now().date(), time())
                today_lists = TodoList.objects.filter((Q(created_by=user) | Q(assigned_to=user)),
                                                      created_date__gte=today_start)
                return today_lists.values()

            elif view_type == 'week':
                week_lists = TodoList.objects.filter((Q(created_by=user) | Q(assigned_to=user)),
                                                     created_date__gte=timezone.now() - timedelta(days=7))
                return week_lists.values()

            else:
                all_lists = TodoList.objects.filter(Q(created_by=user) | Q(assigned_to=user)).values()
                p = Paginator(all_lists, 5)
                return p.page(int(page_num)).object_list
            # return TodoTaskSerializer(lists.values()).data

        except:
            return None

    def accept_task(self, task_id, is_accepted):
        if is_accepted in [False, 'false', 'False']:
            return True
        elif is_accepted in [True, 'true', 'True']:
            accept = TodoList.objects.get(id=task_id)
            accept.isaccepted = True
            accept.save()
            return True
        else:
            return False
        # print(TodoUser.objects.get(auth_token=self.auth_token).name)
        # print(accept.assigned_to)
        # print(accept.assigned_to is TodoUser.objects.get(auth_token=self.auth_token).name)

"""
# Pagination
from django.core.paginator import Paginator
objects = ['john', 'paul', 'george', 'ringo']
p = Paginator(objects, 2)
p.count
p.num_pages
page1 = p.page(1)
page1.object_list
page1.has_next()
page2.has_previous()
"""
