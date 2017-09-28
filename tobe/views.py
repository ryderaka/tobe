from django.shortcuts import render

from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .tobedone.user import UserAuth, UserDetail


@api_view(['GET'])
def otp_generate(request):
    """ Generated OTP valids for 30 seconds """
    phone = request.GET.get('phone', None)
    otp = UserAuth(phone).generate_otp()
    return Response({'phone': phone, 'otp': otp})


@api_view(['GET'])
def otp_verify(request):
    """ Verifies if the User is already registered, OTP verification,
        returns auth_token if user is there else Null """
    phone = request.GET.get('phone', None)
    otp = request.GET.get('otp', None)
    verified, user_exists, auth_token = UserAuth(phone).verify_otp(otp)
    return Response({'phone': phone, 'success': verified, 'is_registered': user_exists, 'auth_token': auth_token})


@api_view(['GET'])
def get_profile(request):
    """ returns user profile details: token, name, phone """
    auth_token = request.GET.get('token', None)
    name, phone = UserDetail(auth_token).get_user_profile()
    if name is not None:
        return Response({'success': True, 'user': {'phone': phone, 'name': name, 'auth_token': auth_token}})
    else:
        return Response({'success': False})


@api_view(['GET', 'POST'])
def new_profile(request):
    """ user enters name and phone and it returns token """
    phone = request.GET.get('phone', None)
    name = request.GET.get('name', None)

    auth_token = UserAuth(phone).user_registration(name)
    if auth_token is not None:
        return Response({'success': True, 'phone': phone, 'auth_token': auth_token})
    else:
        return Response({'success': False})


@api_view(['GET', 'POST'])
def dashboard(request):
    """ dashboard """
    auth_token = request.GET.get('token', None)
    view_type = request.GET.get('type', None)
    # if auth_token:
    pass


@api_view(['GET', 'POST'])
def assign_todo(request):
    """ post todo task details """
    auth_token = request.GET.get('token', None)
    title = request.GET.get('title', None)
    description = request.GET.get('description', None)
    sender = request.GET.get('sender', None)
    receiver = request.GET.get('receiver', None)


@api_view(['GET', 'POST'])
def accept_todo(request):
    """  """



# def user_auth(request, phone_num):
#     queryset = User.objects.all(phone=phone_num)
#     token, created = Token.objects.get_or_create(queryset)
#     return queryset.phone, token.key
