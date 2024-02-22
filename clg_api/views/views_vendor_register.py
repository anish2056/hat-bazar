
from clg_api import custom_exception
from clg_api.models import Category
from clg_api import validations
from user.models import User
from rest_framework.decorators import APIView
from rest_framework import status
from django.db import transaction
from django.http import JsonResponse

from clg_api import globalparamers
import logging


logger = logging.getLogger('django')
# Create your views here.


class VendorRegister(APIView):
    def post(self, request, *args, **kwargs):
        try:
            if not request.body:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.INVALID_REQUEST_BODY,
                }
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
            (json_error, first_name, last_name, username, password, email, date_of_birth,
             gender, phone, toll, address, pan, products) = validations.vendor_register(request)
            if json_error:
                print(json_error,11)
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    "error": json_error
                }
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                user = User.objects.create_user(email=email,
                                                username=username,
                                                phone=phone,
                                                date_of_birth=date_of_birth,
                                                gender=gender,
                                                first_name=first_name,
                                                last_name=last_name,
                                                address=address,
                                                order_location=toll,
                                                pan_number=pan,
                                                user_Type="V"
                                                )
                for product in products:
                    category = Category.objects.get(id=product)
                    user.category.add(category)
                user.set_password(password)
                user.save()
                message = {
                    globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.DATA_CREATE
                }
                return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
