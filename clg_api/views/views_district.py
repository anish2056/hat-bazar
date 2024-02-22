from clg_api import custom_exception
from clg_api.models import District
from rest_framework.decorators import APIView
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate
from django.http import JsonResponse

from clg_api import globalparamers
import logging


logger = logging.getLogger('django')
# Create your views here.


class DistrictListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            province_id = request.query_params.get("data", None)
            districts = District.objects.filter(province_id=province_id)
            district_list = []
            for district in districts:
                district_list.append({
                    "id": district.id,
                    "name": district.name
                })
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": district_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)

