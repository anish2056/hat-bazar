from clg_api import custom_exception
from clg_api.models import Province
from  clg_api import validations
from user.models import  User
from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .import globalparamers
import logging


logger = logging.getLogger('django')
# Create your views here.


class ProvinceListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            provinces = Province.objects.all()
            province_list = []
            for province in provinces:
                province_list.append({
                    "id": province.id,
                    "name": province.name
                })
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": province_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)

