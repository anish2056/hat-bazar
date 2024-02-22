from user.models import User
from pickle import GLOBAL
from .import globalparamers
import json
from rest_framework.authtoken.models import Token

import logging
import base64

from django.http import JsonResponse
from rest_framework import exceptions, status
from django.contrib.auth.hashers import check_password

logger = logging.getLogger('django')


def login_validation(request, pk):
    json_error = []
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']

        print(auth_header)
        encoded_credentials = auth_header.split(' ')[1]
        print("encoded: ", encoded_credentials)
        decoded_credentials = base64.b64decode(
            encoded_credentials).decode("utf-8").split(':')
        print('decode:', decoded_credentials)
        email = decoded_credentials[0]
        print('email:', email)
        password = decoded_credentials[1]
        print('password:', password)
        try:
            user = User.objects.get(email=email, is_active=True)
            if User.objects.filter(email=email, is_active=True).exists():
                user_password = user.password
                match_password = check_password(password, user_password)
                if not match_password:
                    json_error.append("Invalid password.")
                else:
                    pass
            else:
                json_error.append("incorrect email.")

        except User.DoesNotExist as e:
            logger.error(str(e), exc_info=True)
            json_error.append("No such user.")

    except Exception as e:
        logger.error(str(e), exc_info=True)
        json_error.append("No such user.")
    return json_error, email, password


def forgot_password_validation(request, pk):
    json_error = []
    try:
        data = json.loads(request.body)
        email = data['email'] if 'email' in data else ''
        if not email:
            json_error.append("email can not be blank.")
        password_reset = data['forgotPassword'] if 'forgotPassword' in data else ''
        if not password_reset:
            json_error.append("Password can not be blank.")
    except Exception as e:
        logger.error(str(e), exc_info=True)
        json_error.append("No such user.")
    return json_error, email, password_reset


def auth_validation(request):
    json_error = []
    try:
        token = request.META.get('HTTP_AUTHORIZATION', None)
        print('token', token)
        if not token:
            return None, None
        else:
            try:
                token = token.split(' ')[1]
                token = Token.objects.get(key=token)
                if not token:
                    return None, None
                else:
                    try:
                        user = User.objects.get(id=token.user_id)
                        if user:
                            return json_error, user
                        else:
                            return json_error, None
                    except User.DoesNotExist as e:
                        logger.error(str(e), exc_info=True)
                        json_error.append("Unauthorized")
                        return json_error, None
            except Token.DoesNotExist as e:
                logger.error(str(e), exc_info=True)
                json_error.append("Unauthorized")
                return json_error, None

    except Exception as e:
        logger.error(str(e), exc_info=True)
        json_error.append("Unauthorized")
        return json_error, None
