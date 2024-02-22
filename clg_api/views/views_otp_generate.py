import random
import smtplib
from clg_api import custom_exception
from user.models import User
from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate
from django.http import JsonResponse
import base64

from clg_api import globalparamers
import json
import logging


logger = logging.getLogger('django')
# Create your views here.



class OtpGenerateListView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            json_error = []
            data = json.loads(request.body)
            print(data)
            confirm_email = str(data['confirmEmail']).strip(
            ) if 'confirmEmail' in data else ''
            if not confirm_email:
                json_error.append('Email can not be blank')
            else:
                if User.objects.filter(email=confirm_email).exists():
                    pass
                else:
                    json_error.append("Please send correct email.")
            if json_error:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    "error": json_error
                }
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                user = User.objects.get(email=confirm_email)
                globalparamers.CONFIRM_EMAIL.clear()
                globalparamers.CONFIRM_EMAIL.append(user)
                otp1 = ''.join([str(random.randint(0, 9)) for i in range(6)]) #012345
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('anishbista2056@gmail.com', 'lrekhlrgnapjwjkz')
                msg = f"hello{confirm_email} your otp code is {str(otp1)}"
                server.sendmail("anishbista2056@gmail.com", confirm_email, msg)
                server.quit()
                user.otp = otp1
                user.save()
                message = {
                    globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                    "data": user
                }
                return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)


class OtpConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            json_error = []
            data = json.loads(request.body)
            print(data)
            confirm_email = str(data['confirmEmail']).strip(
            ) if 'confirmEmail' in data else ''
            if not confirm_email:
                json_error.append('Email can not be blank')
            else:
                if User.objects.filter(email=confirm_email).exists():
                    pass
                else:
                    json_error.append("Please send correct email.")
            if json_error:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    "error": json_error
                }
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                user = User.objects.get(email=confirm_email)
                globalparamers.CONFIRM_EMAIL = user
                otp = ''.join([str(random.randint(0, 9)) for i in range(6)])
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('anishbista2056@gmail.com', 'lrekhlrgnapjwjkz')
                msg = f"hello{confirm_email} your otp code is {str(otp)}"
                server.sendmail("anishbista2056@gmail.com", confirm_email, msg)
                server.quit()
                user.otp = otp
                user.save()
                message = {
                    globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                }
                return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
