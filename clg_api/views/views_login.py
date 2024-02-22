from clg_api import login_auth
from user.models import  User  
from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .import globalparamers
import logging


logger = logging.getLogger('django')
# Create your views here.


class LoginView(APIView):
    authentication_classes = []  

    def post(self, request, *args, **kwargs):
        try:
            json_error, email, password = login_auth.login_validation(request, None)
            if json_error:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    'error': json_error
                }
                return JsonResponse(message, status=status.HTTP_401_UNAUTHORIZED)
            user = authenticate(request, email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                message = {
                    "username": user.username,
                    "email": user.email,
                    "mobileNumber": user.phone,
                    "token": token.key
                }
                return JsonResponse(message, status=status.HTTP_200_OK)
            else:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: "No such user."
                }
                return JsonResponse(message, status=status.HTTP_401_UNAUTHORIZED)
        except ValueError as e:
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

