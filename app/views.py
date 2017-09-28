from django.shortcuts import render

from todo.app.models import Item, User
from rest_framework.authtoken.models import Token
from .tobedone.user import UserAuth, UserDetail


def otp_generate(request, phone):
    """ it generates OTP thats valids for 30 seconds """
    otp = UserAuth(phone).generate_otp
    return {'phone': phone, 'otp': otp}


def otp_verify(request, phone, otp):
    """ verifies if user is already registered, otp verification,
        returns auth_token if user is there else None """
    verified, user_exists, auth_token = UserAuth(phone).verify_otp(otp)
    return {'phone': phone, 'success': verified, 'is_registered': user_exists, 'auth_token': auth_token}


def get_profile(request, auth_token):
    """ returns user profile details: token, name, phone """
    name, phone = UserDetail(auth_token).get_profile()
    if name is not None:
        return {'success': True, 'user': {'phone': phone, 'name': name, 'auth_token': auth_token}}
    else:
        return {'success': False}


def new_profile(request, phone, name):
    """ user enters name and phone and it returns token """
    auth_token = UserAuth(phone).user_registration(name)
    if auth_token is not None:
        return {'success': True, 'phone': phone, 'auth_token': auth_token}
    else:
        return {'success': False}


def dashboard(request, view_type):
    pass


# def user_auth(request, phone_num):
#     queryset = User.objects.all(phone=phone_num)
#     token, created = Token.objects.get_or_create(queryset)
#     return queryset.phone, token.key
