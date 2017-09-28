# -*- coding: utf-8 -*-

import zlib
import base64
import pyotp
from tobe.models import TodoUser
from django.contrib.auth.models import User


class UserAuth:
    otp_obj = None
    otp = None

    def __init__(self, phone):
        self.phone = phone

    def generate_otp(self):
        otp_obj = pyotp.TOTP(base64.b32encode(zlib.compress(self.phone.encode())))
        otp = otp_obj.now()
        # return {'phone': self.phone, 'otp': self.otp}
        return otp

    def get_auth_token(self):
        return TodoUser.objects.get(phone=self.phone).auth_token

    def verify_otp(self, otp):
        otp_obj = pyotp.TOTP(base64.b32encode(zlib.compress(self.phone.encode())))
        user_exists = TodoUser.objects.filter(phone=self.phone).exists()
        if otp_obj.verify(otp):
            verified = True
            return verified, user_exists, self.get_auth_token() if user_exists else None
            # return {'success': True, 'is_registered': user_exists, 'phone': self.phone, 'auth_token': auth_token}
        else:
            verified = False
            return verified, user_exists, None
            # return {'success': False, 'is_registered': user_exists}

    def user_registration(self, name):
        try:
            TodoUser.objects.create_user(name, self.phone)
            auth_token = self.get_auth_token()
            return auth_token
        except:
            return None


class UserDetail:
    def __init__(self, token):
        self.token = token

    def get_user_profile(self):
        try:
            name = User.objects.get(auth_token=self.token).username
            phone = User.objects.get(auth_token=self.token).phone
            # phone = 11
            return name, phone
        except:
            return None, None
