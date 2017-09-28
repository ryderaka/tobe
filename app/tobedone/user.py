# -*- coding: utf-8 -*-

import zlib
import base64
import pyotp
from todo.app.models import User


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
        return User.objects.get(phone=self.phone).auth_token

    def verify_otp(self, otp):
        otp_obj = pyotp.TOTP(base64.b32encode(zlib.compress(self.phone.encode())))
        user_exists = User.objects.filter(phone=self.phone).exists()
        if otp_obj.verify(otp):
            verified = True
            auth_token = self.get_auth_token()
            return verified, user_exists, auth_token
            # return {'success': True, 'is_registered': user_exists, 'phone': self.phone, 'auth_token': auth_token}
        else:
            verified = False
            return verified, user_exists, None
            # return {'success': False, 'is_registered': user_exists}

    def user_registration(self, name):
        try:
            User.objects.create_user(name, self.phone)
            auth_token = self.get_auth_token()
            return auth_token
        except:
            return None


class UserDetail:
    def __init__(self, token):
        self.token = token

    def get_profile(self):
        try:
            name = User.objects.get(auth_token=self.token).username
            phone = User.objects.get(auth_token=self.token).phone
            return {'name': name, 'phone': phone}
        except:
            return {'name': None, 'phone': None}

