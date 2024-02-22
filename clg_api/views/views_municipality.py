
from clg_api import custom_exception
from clg_api.models import Municipality
from rest_framework.decorators import APIView
from rest_framework import status
from django.http import JsonResponse

from .import globalparamers
import json
import logging


logger = logging.getLogger('django')
# Create your views here.


class MunicipalityListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            province_id = request.query_params.get("data", None)
            district_id = request.query_params.get("data1", None)
            municipalitys = Municipality.objects.filter(
                province_id=province_id, district_id=district_id)
            municipality_list = []
            for municipality in municipalitys:
                municipality_list.append({
                    "id": municipality.id,
                    "name": municipality.name
                })
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": municipality_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)

