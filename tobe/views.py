from django.shortcuts import render

from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework.response import Response
from .tobedone.user import UserAuth, UserDetail
from .tobedone.task import Tasks

"""
# Firebase for notification
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AIzaSyAJFx9EROoFX1lk64Lavt9hkkJsLaqHqro")
registration_id = "<device registration_id>"
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
print(result)
"""


def get_registration_id(request):
    pass


@api_view(['GET'])
def otp_generate(request):
    """ Generated OTP valids for 30 seconds """
    phone = request.GET.get('phone', None)
    otp = UserAuth(phone).generate_otp()
    return Response(
        {
            'success': True,
            'phone': phone,
            'otp': otp
        }
    )


@api_view(['GET'])
def otp_verify(request):
    """ Verifies if the User is already registered, OTP verification,
        returns auth_token if user is there else Null """
    phone = request.GET.get('phone', None)
    otp = request.GET.get('otp', None)
    verified, user_exists, auth_token, user_id = UserAuth(phone).verify_otp(otp)
    return Response(
        {
            'phone': phone,
            'success': verified,
            'is_registered': user_exists,
            'auth_token': auth_token,
            'user_id': user_id
        }
    )


@api_view(['POST'])
def new_profile(request):
    """ user enters name and phone and it returns token """
    phone = request.POST.get('phone', None)
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    auth_token, user_id = UserAuth(phone).user_registration(name, email)

    if auth_token is not None:
        return Response(
            {
                'success': True,
                'phone': phone,
                'auth_token': auth_token,
                'user_id': user_id
            }
        )

    else:
        return Response(
            {
                'success': False
            }
        )


@api_view(['GET'])
def get_profile(request):
    """ returns user profile details: token, name, phone """
    auth_token = request.META.get('HTTP_TOKEN', None)
    name, phone = UserDetail(auth_token).get_user_profile()

    if name is not None:
        return Response(
            {
                'success': True,
                'user':
                    {
                        'phone': phone,
                        'name': name,
                        'auth_token': auth_token
                    }
            }
        )

    else:
        return Response(
            {
                'success': False
            }
        )


@api_view(['POST'])
def create_todo(request):
    """ Create New Task """
    auth_token = request.META.get('HTTP_TOKEN', None)
    title = request.POST.get('title', None)
    description = request.POST.get('description', None)
    receiver = request.POST.get('receiver', None)
    due_date = request.POST.get('due_date', None)
    assigned_date = timezone.now() if receiver is not None else None
    result = Tasks(auth_token).create_task(receiver, title, description, assigned_date, due_date)
    return Response(
        {
            'success': result
        }
    )


@api_view(['GET'])
def dashboard(request):
    """ Dashboard """
    auth_token = request.META.get('HTTP_TOKEN', None)
    view_type = request.GET.get('type', None)
    page_num = request.GET.get('page', None)
    result = Tasks(auth_token).dashboard(view_type, page_num)

    if result is not None:
        return Response(
            {
                'success': True,
                'data': result
            }
        )

    else:
        return Response(
            {
                'success': False
            }
        )


@api_view(['GET', 'POST'])
def accept_todo(request):
    """ Receiver has to accept or reject the task assigned """
    auth_token = request.META.get('HTTP_TOKEN', None)
    todoid = request.POST.get('todo_id', None)
    isaccepted = request.POST.get('is_accepted', None)
    result = Tasks(auth_token=auth_token).accept_task(todoid, isaccepted)
    return Response(
        {
            'success': result
        }
    )



### Notification ###

# https://ampersandacademy.com/tutorials/ionic-framework-version-2/automate-push-notification-using-python-and-firebase-cloud-messaging
# https://pypi.python.org/pypi/pyfcm/
