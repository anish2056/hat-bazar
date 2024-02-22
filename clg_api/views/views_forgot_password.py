import random
import smtplib
from clg_api import login_auth
from user.models import User
from rest_framework.decorators import APIView
from rest_framework import status
from django.http import JsonResponse

from .import globalparamers
import logging

logger = logging.getLogger('django')
# Create your views here.

class ForgorPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.body:
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.NO_REQUEST_BODY
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            json_error, email, password = login_auth.forgot_password_validation(
                request, None)
            if json_error:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    "error": json_error
                }
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(email=email, is_active=True)
            if user.exists():
                try:
                    user = User.objects.get(email=email, is_active=True)
                    user.set_password(password)
                    user.save()
                    message = {
                        "resut_code": "password successfully changed."
                    }
                    return JsonResponse(message, status=status.HTTP_200_OK)
                except User.DoesNotExist as e:
                    logger.error(str(e), exc_info=True)
                    message = {
                        globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                        globalparamers.RESULT_DESCRIPTION: globalparamers.ID_DOES_NOT_EXIT,
                    }
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    "error": json_error
                }
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)

