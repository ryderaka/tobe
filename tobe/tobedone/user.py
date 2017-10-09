# -*- coding: utf-8 -*-

import zlib
import pyotp
import base64
import tokenlib
from tobe.models import TodoUser
# from django.contrib.auth.models import User


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
        user = TodoUser.objects.get(phone=self.phone)
        return user.auth_token, user.id

    def verify_otp(self, otp):
        otp_obj = pyotp.TOTP(base64.b32encode(zlib.compress(self.phone.encode())))
        user_exists = TodoUser.objects.filter(phone=self.phone).exists()
        if otp_obj.verify(otp):
            verified = True
            if user_exists:
                token, user_id = self.get_auth_token()
            else:
                token = user_id = None
            return verified, user_exists, token, user_id
            # return {'success': True, 'is_registered': user_exists, 'phone': self.phone, 'auth_token': auth_token}
        else:
            verified = False
            return verified, user_exists, None, None
            # return {'success': False, 'is_registered': user_exists}

    def create_token(self):
        token = tokenlib.make_token({"phone": self.phone}, secret="WEARECHIMP")
        # data = tokenlib.parse_token(token, secret="WEARECHIMP")
        return token

    def user_registration(self, name, email):
        try:
            user = TodoUser(phone=self.phone, name=name, email=email)
            token = self.create_token()
            user.auth_token = token
            try:
                user.save()
            except Exception as e:
                print(e)
                return None, None
            user_id = TodoUser.objects.get(phone=self.phone).id
            return token, user_id
        except:
            return None, None


class UserDetail:
    def __init__(self, token):
        self.token = token

    def get_user_profile(self):
        try:
            user = TodoUser.objects.get(auth_token=self.token)
            return user.name, user.phone
        except:
            return None, None
