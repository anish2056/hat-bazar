from clg_api.models import Product
from clg_api import validations
from user.models import User
from rest_framework.decorators import APIView
from rest_framework import status
from django.http import JsonResponse

from clg_api import globalparamers
import logging


logger = logging.getLogger('django')
# Create your views here.


class VendorSignupView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.body:
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.NO_REQUEST_BODY
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            (json_error, name, description,
             product_prize, manufactured_date, image) = validations.product_validation(request, None)
            if json_error:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    "error": json_error
                }
                return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
            import datetime
            created_by = User.objects.get(
                id='ba7d387f38964f1fb62e1e5c5b3b3b6b')
            Product.objects.create(name=name,
                                   price=product_prize,
                                   description=description,
                                   photo=image,
                                   date_created=datetime.datetime.now(),
                                   created_by=created_by
                                   )
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.DATA_CREATE
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
